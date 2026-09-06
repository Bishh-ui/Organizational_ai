---
title: Organizational AI
emoji: 🏦
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: "4.20.0"
app_file: app.py
pinned: false
license: mit
---

# Organizational AI — Policy Assistant

AI-powered Q&A over organizational policy documents.  
Grounded answers via RAG (Retrieval-Augmented Generation) + TinyLlama fine-tuned with REINFORCE RL.

## How it works

1. Policy PDFs are processed into a text corpus
2. At query time, the top-3 relevant passages are retrieved via sentence embeddings
3. TinyLlama generates an answer grounded only in those passages
4. Three DistilBERT discriminators (factuality, style, safety) penalize hallucinated output during training

## Tabs

| Tab | What it does |
|---|---|
| 💬 Chat | Ask questions about your policies |
| 📄 Upload | Upload new PDF/TXT policy documents |
| 🔐 Login | Log in and track session history |
| 🔧 Admin | View user statistics (PIN protected) |

## Running locally

```bash
pip install -r gradio_app/requirements.txt
python gradio_app/app.py
```

Then open http://localhost:7860
