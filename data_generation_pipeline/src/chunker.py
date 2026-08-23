from typing import List


def chunk_text(text: str, chunk_size: int = 120, overlap: int = 30) -> List[str]:
    """Split text into overlapping word-level chunks.

    Args:
        text: Input text to split.
        chunk_size: Number of words per chunk.
        overlap: Number of words to overlap between consecutive chunks.

    Returns:
        List of chunk strings.
    """
    if not text:
        return []

    words = text.split()
    if len(words) <= chunk_size:
        return [" ".join(words)]

    chunks: List[str] = []
    step = chunk_size - overlap
    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i : i + chunk_size]))
        i += step

    return chunks
