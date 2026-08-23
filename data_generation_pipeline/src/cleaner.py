import re

# Prompt-leakage markers that indicate the model bled into its own output
_BAD_MARKERS = ("Human:", "You are generating", "<question>", "<answer>")


def clean_text(t: str) -> str:
    """Normalize raw document text for chunking and Q/A generation.

    Steps applied (in order):
    - Normalize line endings
    - Strip non-ASCII characters
    - Remove content before TABLE OF CONTENTS
    - Remove TOC and mini-TOC blocks
    - Remove PREFACE section
    - Remove OCR-style spaced footers (e.g. "A m a n a h")
    - Collapse excessive blank lines and whitespace
    """
    if not t:
        return ""

    # Normalize line endings
    t = re.sub(r"\r\n?", "\n", t)

    # Strip non-ASCII to reduce tokenization surprises
    t = re.sub(r"[^\x00-\x7F]+", " ", t)

    # Drop everything before TABLE OF CONTENTS if present
    t = re.sub(
        r"^[\s\S]*?TABLE OF CONTENTS", "TABLE OF CONTENTS", t, flags=re.IGNORECASE
    )

    # Remove TOC region (best-effort, non-fatal)
    try:
        t = re.sub(r"TABLE OF CONTENTS[\s\S]*?GLOSSARY[\s\.]*388", "", t)
    except Exception:
        pass

    # Remove mini-TOC blocks (6+ lines of "Title  x.y.z" patterns)
    t = re.sub(
        r"(?:\n|^)(?:[A-Za-z][A-Za-z0-9\s\(\)/,&\-]+?\s+\d+(?:\.\d+)+\s*){6,}",
        "\n",
        t,
        flags=re.MULTILINE,
    )

    # Remove residual mini-TOC lines inside section 1.1
    m = re.search(
        r"(1\.1\s+OVERVIEW[\s\S]*?)(\n1\.2\s+CURRENT\s+ACCOUNTS)",
        t,
        flags=re.IGNORECASE,
    )
    if m:
        section_11 = re.sub(r"(?m)^[^\n]*\b\d+\.\d+\.\d+\s*$", "", m.group(1))
        t = section_11.strip() + "\n\n" + t[m.end(1):].strip()

    # Remove PREFACE up to first SECTION / CHAPTER heading
    t = re.sub(
        r"PREFACE[\s\S]*?(SECTION\s+1|CHAPTER\s+1)", r"\1", t, flags=re.IGNORECASE
    )

    # Remove OCR-style spaced text footers (e.g. "A m a n a h  B a n k")
    t = re.sub(r"(?m)^(?:\s*(?:[A-Za-z]\s+){2,}[A-Za-z].*)$", "", t)

    # Collapse blank lines and extra whitespace
    t = re.sub(r"(?m)^\s*$", "", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    t = re.sub(r"[ \t]{2,}", " ", t)

    return t.strip()


def clean_text_leakage(text: str) -> str:
    """Return empty string if the text contains prompt-leakage markers, else strip it."""
    for marker in _BAD_MARKERS:
        if marker in text:
            return ""
    return text.strip()
