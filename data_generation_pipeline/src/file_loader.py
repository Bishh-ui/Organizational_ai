from pathlib import Path
from typing import List

import PyPDF2


def _extract_pdf(path: str) -> str:
    """Extract plain text from all pages of a PDF file."""
    pages: List[str] = []
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            pages.append(page.extract_text() or "")
    return "\n".join(pages)


def extract_text(file_path: str) -> str:
    """Extract text from a PDF or TXT file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file type is not supported.
    """
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    suffix = p.suffix.lower()
    if suffix == ".pdf":
        return _extract_pdf(file_path)
    if suffix == ".txt":
        return p.read_text(encoding="utf-8")
    raise ValueError(f"Unsupported file type '{suffix}'. Provide a .pdf or .txt file.")


def discover_files(input_path: str) -> List[Path]:
    """Return a sorted list of all PDF and TXT files at the given path.

    If input_path is a single file, returns it directly.
    If it is a directory, recursively discovers all .pdf and .txt files.

    Raises:
        FileNotFoundError: If the path does not exist.
    """
    p = Path(input_path)
    if not p.exists():
        raise FileNotFoundError(f"Input path not found: {input_path}")

    if p.is_file():
        return [p]

    files: List[Path] = []
    for ext in ("*.pdf", "*.txt"):
        files.extend(p.rglob(ext))

    return sorted(files)


def get_file_name_from_dir(input_path: str) -> str:
    """Return the stem (filename without extension) of the given path."""
    return Path(input_path).stem
