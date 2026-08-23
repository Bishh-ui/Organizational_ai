from typing import List

from sentence_transformers import SentenceTransformer, util

_embed_model: SentenceTransformer = None


def _get_embed_model(model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> SentenceTransformer:
    """Return a cached SentenceTransformer, loading it on first call."""
    global _embed_model
    if _embed_model is None:
        _embed_model = SentenceTransformer(model_name)
    return _embed_model


def semantic_dedupe(qas: List[dict], threshold: float = 0.88) -> List[dict]:
    """Remove near-duplicate Q/A pairs using cosine similarity on question embeddings.

    Args:
        qas: List of Q/A dicts, each with a "question" key.
        threshold: Cosine similarity threshold above which two questions are duplicates.

    Returns:
        Deduplicated list preserving the first occurrence of each cluster.
    """
    if not qas:
        return []

    model = _get_embed_model()
    questions = [entry["question"] for entry in qas]
    q_embs = model.encode(questions, convert_to_tensor=True)

    used = [False] * len(questions)
    keep: List[dict] = []

    for i, qa in enumerate(qas):
        if used[i]:
            continue
        keep.append(qa)
        sims = util.cos_sim(q_embs[i], q_embs).cpu().numpy()[0]
        for j in range(i + 1, len(questions)):
            if sims[j] >= threshold:
                used[j] = True

    return keep
