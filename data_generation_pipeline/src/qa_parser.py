import re
from typing import List, Tuple

_Q_RE = re.compile(r"^\s*Q\s*(\d+)\s*[:.\-]\s*(.+?)(\?)?\s*$", re.IGNORECASE)
_A_RE = re.compile(r"^\s*A\s*(\d+)\s*[:.\-]\s*(.+)", re.IGNORECASE)


def parse_qa_block(block: str) -> List[Tuple[str, str]]:
    """Parse a model output block into a list of (question, answer) pairs.

    Expects lines formatted as:
        Q1: <question>?
        A1: <answer>

    Pairs are only accepted when the Q and A indices match.
    """
    lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
    pairs: List[Tuple[str, str]] = []
    i = 0

    while i < len(lines) - 1:
        q_match = _Q_RE.match(lines[i])
        a_match = _A_RE.match(lines[i + 1])

        if q_match and a_match and q_match.group(1) == a_match.group(1):
            q = q_match.group(2).strip()
            # Trim any trailing Q/A content that leaked into the answer
            a = re.split(r"\nQ\d+[:\-]|Q\d+[:\-]", a_match.group(2))[0].strip()
            pairs.append((q, a))
            i += 2
        else:
            i += 1

    return pairs
