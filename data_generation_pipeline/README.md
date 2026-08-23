# data-pipeline

A modular, production-ready Question & Answer (Q/A) generation pipeline for bank policy documents.
Transforms large policy PDFs into validated Q/A pairs using LLMs, evidence extraction, and semantic deduplication.

---

## Features

- PDF and TXT text extraction
- Advanced cleaning tailored for policy documents
- Configurable chunking with overlap
- 4-bit quantized LLM inference via `bitsandbytes` (default: `microsoft/phi-2`)
- Deterministic + sampling generation with automatic retry
- Strict question validation (rejects vague, context-dependent questions)
- Q/A parsing with numbered-pattern matching
- Sentence-level evidence extraction using `sentence-transformers`
- Exact and semantic deduplication (FAISS cosine similarity)
- Fully modular source layout
- CLI interface for terminal execution

---

## Project Structure

```
data_generation_pipeline/
├── README.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── config/
│   ├── pipeline_config.yaml    # chunk size, Q/A limits, dedupe threshold, paths
│   └── model_config.yaml       # model name, embedding model, quantization options
├── src/
│   ├── __init__.py
│   ├── cli.py
│   ├── pipeline_runner.py
│   ├── file_loader.py
│   ├── cleaner.py
│   ├── chunker.py
│   ├── prompts.py
│   ├── model_loader.py
│   ├── generator.py
│   ├── qa_parser.py
│   ├── validators.py
│   ├── evidence.py
│   └── dedupe.py
├── notebooks/
│   └── experiments.ipynb
├── tests/
│   ├── test_cleaner.py
│   ├── test_chunker.py
│   └── test_parser.py
└── docs/
    └── architecture.md
```

---

## Installation

```bash
python3 -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

---

## Input Files

Place your input files (PDF or TXT) inside `data/raw/`. Example:

```
data/raw/amanah_bank_policy.pdf
```

The default `input_path` in `config/pipeline_config.yaml` points to `data/raw/`. Update it if your files are elsewhere.

---

## Running the Pipeline

```bash
# Using config defaults
python -m cli run

# Override input/output from the command line
python -m cli run \
    --input data/raw/amanah_bank_policy.pdf \
    --output data/output/results.json
```

The pipeline will:

1. Extract text from each document
2. Clean and normalize the text
3. Split into overlapping chunks
4. Generate Q/A pairs per chunk via the configured LLM
5. Extract supporting evidence sentences
6. Deduplicate similar questions (semantic + exact)
7. Save results as JSON

---

## Configuration

| File | Purpose |
|---|---|
| `config/pipeline_config.yaml` | Chunk size, Q/A limits, dedupe threshold, input/output paths |
| `config/model_config.yaml` | Model name, embedding model, quantization settings |

---

## Running Tests

```bash
pytest -q
```

---

## Notebooks

Use `notebooks/` for debugging, exploring chunks, visualizing embeddings, or evaluating model output.

---

## Contributing

Pull requests welcome. Follow standard Git branching with PR review.

---

## License

Open-source — free to use and modify.
