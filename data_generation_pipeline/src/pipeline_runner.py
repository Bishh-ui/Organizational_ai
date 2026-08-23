import json
from collections import defaultdict
from typing import Any

from config_reader import load_config
from dedupe import semantic_dedupe
from document_reader import process_document
from file_loader import discover_files
from model_loader import load_model_tokenizer

_base_cfg = (load_config("config/pipeline_config.yaml") or {}) | (
    load_config("config/model_config.yaml") or {}
)
DEFAULT_MODEL = _base_cfg.get("default_model", "meta-llama/Llama-3.2-1B")
SEMANTIC_DEDUPE_THRESHOLD = _base_cfg.get("semantic_dedupe_threshold", 0.88)


def run_pipeline(input_path: str, out_file: str, cfg: dict = None) -> None:
    cfg = cfg or _base_cfg

    files = discover_files(input_path)
    print(f"[INFO] Found {len(files)} files")

    model_name = cfg.get("default_model", DEFAULT_MODEL)
    quant_config = cfg.get("quantization", {})
    dedupe_threshold = cfg.get("semantic_dedupe_threshold", SEMANTIC_DEDUPE_THRESHOLD)

    print("[INFO] Loading model and tokenizer (device_map='auto') — this may take a minute...")
    tokenizer, model = load_model_tokenizer(model_name, quant_config)

    all_results: list = []
    report: dict[str, Any] = {
        "files_found": len(files),
        "files_processed": 0,
        "files_failed": 0,
        "qas_per_document": {},
    }

    for f in files:
        print(f"[INFO] Processing {f.name}")
        results, status = process_document(f, tokenizer, model)

        if status["status"] == "success":
            report["files_processed"] += 1
            report["qas_per_document"][f.name] = status["qas"]
            all_results.extend(results)
        else:
            report["files_failed"] += 1
            print(f"[WARN] Failed {f.name}: {status['error']}")

    # --- Semantic deduplication per document ---
    print("[INFO] Running semantic dedupe per document...")
    docs: dict = defaultdict(list)
    for qa in all_results:
        docs[qa["doc_id"]].append(qa)

    deduped_results: list = []
    for _, qas in docs.items():
        deduped_results.extend(semantic_dedupe(qas, threshold=dedupe_threshold))

    print(f"[INFO] Q/A count after per-document semantic dedupe: {len(deduped_results)}")

    # --- Global exact deduplication ---
    final_results: list = []
    seen: set = set()
    for qa in deduped_results:
        key = (qa["question"].lower(), qa["answer"].lower())
        if key not in seen:
            seen.add(key)
            final_results.append(qa)

    print(f"[INFO] Final Q/A count after global exact dedupe: {len(final_results)}")

    # --- Save results ---
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(final_results, f, indent=2, ensure_ascii=False)
    print(f"[INFO] Saved final dataset -> {out_file}")

    report["total_qas"] = len(final_results)

    with open("processing_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print("[INFO] Saved processing_report.json")

    print("[INFO] Pipeline complete.")
