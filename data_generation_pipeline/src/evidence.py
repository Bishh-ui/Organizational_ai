from typing import List

import nltk
from sentence_transformers import SentenceTransformer, util

_embed_model: SentenceTransformer = None


def _get_embed_model(model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> SentenceTransformer:
    """Return a cached SentenceTransformer, loading it on first call."""
    global _embed_model
    if _embed_model is None:
        _embed_model = SentenceTransformer(model_name)
    return _embed_model


def _tokenize_sentences(text: str) -> List[str]:
    """Tokenize text into sentences using NLTK, downloading data if needed."""
    for resource in ("tokenizers/punkt_tab", "tokenizers/punkt"):
        try:
            nltk.data.find(resource)
            break
        except LookupError:
            pkg = resource.split("/")[1]
            try:
                nltk.download(pkg, quiet=True)
                break
            except Exception:
                continue

    from nltk.tokenize import sent_tokenize
    return [s.strip() for s in sent_tokenize(text) if s.strip()]


def extract_evidence_sentences(
    answer: str,
    chunk: str,
    k: int = 2,
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
) -> List[str]:
    """Return the top-k sentences from chunk most similar to the answer.

    Args:
        answer: The answer string to match against.
        chunk: Source passage to extract evidence from.
        k: Maximum number of evidence sentences to return.
        model_name: SentenceTransformer model to use for embeddings.

    Returns:
        List of evidence sentences with cosine similarity > 0.1.
    """
    sents = _tokenize_sentences(chunk)
    if not sents:
        return []

    model = _get_embed_model(model_name)
    embeddings = model.encode([answer] + sents, convert_to_tensor=True)
    ans_emb = embeddings[0]
    sent_embs = embeddings[1:]

    scores = util.cos_sim(ans_emb, sent_embs)[0].cpu().numpy()
    top_idxs = scores.argsort()[::-1][:k]
    return [sents[i] for i in top_idxs if scores[i] > 0.1]
