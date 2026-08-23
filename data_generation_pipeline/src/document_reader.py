import re
import time
from pathlib import Path
from typing import Dict, List, Tuple

from chunker import chunk_text
from cleaner import clean_text, clean_text_leakage
from config_reader import load_config
from evidence import extract_evidence_sentences
from file_loader import extract_text, get_file_name_from_dir
from generator import generate_with_retry
from prompts import build_prompt
from qa_parser import parse_qa_block
from validators import valid_question

_cfg = load_config("config/pipeline_config.yaml") or {}
SLEEP_BETWEEN_CHUNKS: float = _cfg.get("sleep_between_chunks", 0.12)

VAGUE_PATTERNS = [
    r"\bthis policy\b",
    r"\bthis context\b",
    r"\bthis document\b",
    r"\bthis section\b",
    r"\bthe above\b",
    r"\bhere\b",
]


def process_document(file_path: Path, tokenizer, model) -> Tuple[List[Dict], Dict]:
    """Extract, clean, chunk, and generate Q/A pairs for a single document.

    Returns:
        A tuple of (list of Q/A dicts, status dict).
    """
    doc_meta = {
        "doc_id": f"doc_{hash(str(file_path)) & 0xFFFFFFFF}",
        "file_name": file_path.name,
        "file_path": str(file_path),
        "file_type": file_path.suffix.lower().lstrip("."),
    }

    try:
        print(f"[INFO] Loading text of {file_path}...")
        raw = extract_text(str(file_path))
        cleaned = clean_text(raw)

        file_name = get_file_name_from_dir(str(file_path))

        # Save cleaned text for audit purposes
        corpus_path = f"cleaned_corpus_{file_name}.txt"
        with open(corpus_path, "w", encoding="utf-8") as f:
            f.write(cleaned)
        print(f"[INFO] Saved {corpus_path}")

        chunks = chunk_text(cleaned)
        results: List[Dict] = []
        seen_exact: set = set()

        for idx, chunk in enumerate(chunks[:30]):
            prompt = build_prompt(chunk)
            text = generate_with_retry(tokenizer, model, prompt)
            print(f"[INFO] Chunk {idx + 1}/{min(len(chunks), 30)} — {file_name}")

            if not text:
                print(f"[WARN] Empty model output for chunk {idx}")
                time.sleep(SLEEP_BETWEEN_CHUNKS)
                continue

            parsed = parse_qa_block(text)
            if not parsed:
                time.sleep(SLEEP_BETWEEN_CHUNKS)
                continue

            for q, a in parsed:
                q = clean_text_leakage(q)
                a = clean_text_leakage(a)

                if not q or not a:
                    continue
                if q.startswith("<") or a.startswith("<"):
                    continue
                if any(re.search(p, q.lower()) for p in VAGUE_PATTERNS):
                    continue
                if len(a.split()) > 60:
                    continue

                q_norm = q.strip().rstrip("?")
                a_norm = a.strip()

                if not valid_question(q_norm):
                    continue

                key = (q_norm.lower(), a_norm.lower())
                if key in seen_exact:
                    continue
                seen_exact.add(key)

                evidences = extract_evidence_sentences(a_norm, chunk)
                results.append(
                    {
                        **doc_meta,
                        "chunk_id": idx,
                        "question": q_norm,
                        "answer": a_norm,
                        "supporting_passages": evidences or [chunk],
                    }
                )

        return results, {"status": "success", "qas": len(results)}

    except Exception as e:
        return [], {"status": "failed", "error": str(e)}
