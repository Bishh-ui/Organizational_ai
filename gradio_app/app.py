"""
Organizational AI — Gradio web interface
Drop-in replacement for the pywebview desktop frontend.
Runs locally or on Hugging Face Spaces.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

import gradio as gr

# ── make sure the project root is importable ─────────────────────────────────
HERE = Path(__file__).resolve().parent          # gradio_app/
ROOT = HERE.parent                              # project root
sys.path.insert(0, str(ROOT))

from hallucination_reduction.inference import (  # noqa: E402
    build_embeddings,
    generate_answer,
    load_corpus,
    load_model,
    retrieve_relevant_chunks,
)

# ── paths ─────────────────────────────────────────────────────────────────────
CORPUS_PATH  = str(ROOT / "data" / "processed" / "corpus.txt")
RAW_DATA_DIR = str(ROOT / "data" / "raw")
ADMIN_PIN    = os.environ.get("ADMIN_PIN", "9999")

# ── lazy-loaded model state ───────────────────────────────────────────────────
_model            = None
_tokenizer        = None
_device           = None
_docs             = None
_embedder         = None
_corpus_embeddings = None


def _ensure_model():
    """Load model and corpus once; reuse on every subsequent call."""
    global _model, _tokenizer, _device, _docs, _embedder, _corpus_embeddings
    if _model is None:
        _model, _tokenizer, _device = load_model()
        _docs = load_corpus(CORPUS_PATH)
        _embedder, _corpus_embeddings = build_embeddings(_docs, device=str(_device))
    return _model, _tokenizer, _device, _docs, _embedder, _corpus_embeddings


# ── chat logic ────────────────────────────────────────────────────────────────
def chat(message: str, history: list) -> str:
    if not message.strip():
        return "Please enter a question."
    try:
        model, tokenizer, device, docs, embedder, corpus_embs = _ensure_model()
        retrieved = retrieve_relevant_chunks(message, embedder, corpus_embs, docs)
        answer = generate_answer(model, tokenizer, device, message, retrieved)
        return answer.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"


# ── file upload logic ─────────────────────────────────────────────────────────
def handle_upload(files) -> str:
    if not files:
        return "No files selected."

    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    saved = []
    for f in files:
        dest = os.path.join(RAW_DATA_DIR, os.path.basename(f.name))
        with open(f.name, "rb") as src, open(dest, "wb") as dst:
            dst.write(src.read())
        saved.append(os.path.basename(f.name))

    return (
        f"✅ Uploaded {len(saved)} file(s): {', '.join(saved)}\n\n"
        "To re-train the model on the new documents, run:\n"
        "```\npython -m hallucination_reduction.main\n```"
    )


# ── admin logic ───────────────────────────────────────────────────────────────
_login_log: dict = {}


def log_login(name: str, email: str) -> dict:
    """Record a login event (called from the login tab)."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if name not in _login_log:
        _login_log[name] = {"email": email, "logins": []}
    _login_log[name]["logins"].append(ts)
    _login_log[name]["logins"] = _login_log[name]["logins"][-50:]
    return {"status": "ok", "timestamp": ts}


def admin_stats(pin: str) -> str:
    if pin != ADMIN_PIN:
        return "❌ Wrong PIN."

    if not _login_log:
        return "No login data recorded yet."

    lines = [f"**Total users:** {len(_login_log)}\n"]
    total = sum(len(v['logins']) for v in _login_log.values())
    lines.append(f"**Total logins:** {total}\n\n---\n")

    for user, data in _login_log.items():
        last = data["logins"][-1] if data["logins"] else "—"
        lines.append(
            f"**{user}** ({data['email']})  \n"
            f"Logins: {len(data['logins'])} | Last: {last}\n"
        )
    return "\n".join(lines)


# ── UI ────────────────────────────────────────────────────────────────────────
CSS = """
#logo { text-align: center; margin-bottom: 8px; }
#logo h1 { font-size: 2rem; font-weight: 700; color: #1a56db; }
#logo p  { color: #6b7280; }
.tab-nav button { font-weight: 600; }
"""

with gr.Blocks(css=CSS, title="Organizational AI") as demo:

    # ── header ────────────────────────────────────────────────────────────────
    with gr.Row(elem_id="logo"):
        gr.HTML("""
            <h1>🏦 Organizational AI</h1>
            <p>AI-powered policy assistant — grounded answers, no hallucinations</p>
        """)

    with gr.Tabs():

        # ── Chat tab ──────────────────────────────────────────────────────────
        with gr.Tab("💬 Chat"):
            gr.Markdown(
                "Ask anything about your organization's policies. "
                "Answers are grounded in the uploaded documents."
            )
            chatbot = gr.ChatInterface(
                fn=chat,
                chatbot=gr.Chatbot(height=480, bubble_full_width=False),
                textbox=gr.Textbox(
                    placeholder="e.g. What is the KYC procedure for new accounts?",
                    lines=2,
                ),
                examples=[
                    "What documents are required to open a new account?",
                    "What is the AML policy for suspicious transactions?",
                    "How long does KYC verification take?",
                ],
                retry_btn="🔁 Retry",
                undo_btn="↩ Undo",
                clear_btn="🗑 Clear",
            )

        # ── Upload tab ────────────────────────────────────────────────────────
        with gr.Tab("📄 Upload Documents"):
            gr.Markdown(
                "Upload new policy PDFs or TXT files. "
                "After uploading, re-run the data pipeline and training to update the model."
            )
            upload_input = gr.File(
                label="Select files",
                file_types=[".pdf", ".txt"],
                file_count="multiple",
            )
            upload_btn    = gr.Button("Upload", variant="primary")
            upload_status = gr.Markdown()

            upload_btn.click(
                fn=handle_upload,
                inputs=upload_input,
                outputs=upload_status,
            )

        # ── Login tab ─────────────────────────────────────────────────────────
        with gr.Tab("🔐 Login"):
            gr.Markdown("Enter your name and email to log in and start chatting.")
            with gr.Row():
                login_name  = gr.Textbox(label="Name",  placeholder="Your name")
                login_email = gr.Textbox(label="Email", placeholder="you@example.com")
            login_btn    = gr.Button("Log In", variant="primary")
            login_status = gr.Markdown()

            def _do_login(name, email):
                if not name.strip() or not email.strip():
                    return "⚠️ Please enter both name and email."
                result = log_login(name.strip(), email.strip())
                return f"✅ Welcome, **{name}**! Logged in at {result['timestamp']}."

            login_btn.click(
                fn=_do_login,
                inputs=[login_name, login_email],
                outputs=login_status,
            )

        # ── Admin tab ─────────────────────────────────────────────────────────
        with gr.Tab("🔧 Admin"):
            gr.Markdown("View login statistics. Admin PIN required.")
            admin_pin_input = gr.Textbox(
                label="Admin PIN",
                type="password",
                placeholder="Enter PIN",
            )
            admin_btn    = gr.Button("View Stats", variant="secondary")
            admin_output = gr.Markdown()

            admin_btn.click(
                fn=admin_stats,
                inputs=admin_pin_input,
                outputs=admin_output,
            )

    gr.Markdown(
        "<center><small>Organizational AI — powered by TinyLlama + RAG | "
        "<a href='https://huggingface.co/' target='_blank'>Hugging Face Spaces</a></small></center>"
    )


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
        share=False,
    )
