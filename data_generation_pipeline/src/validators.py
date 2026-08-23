import re

_VAGUE_PHRASES = (
    "what is this policy",
    "what does the policy say",
    "what is the purpose of this policy",
)


def valid_question(q: str) -> bool:
    """Return True if the question is specific enough to be useful for training.

    Rejects questions that are too short or rely on vague, context-dependent phrasing.
    """
    if len(q.strip()) < 8:
        return False
    ql = q.lower()
    return not any(phrase in ql for phrase in _VAGUE_PHRASES)
