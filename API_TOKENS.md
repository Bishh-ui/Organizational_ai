# 🔑 API Tokens Guide

This guide explains what API tokens you need and where to configure them.

---

## 🎯 Do I Need an API Token?

### ✅ **NO TOKEN NEEDED** (Current Setup)

Your app uses **public models** that don't require authentication:
- **TinyLlama-1.1B-Chat** (Generator)
- **DistilBERT** (Discriminators)
- **all-MiniLM-L6-v2** (Sentence embeddings)

**You can deploy right now without any tokens!** 🎉

### ⚠️ **TOKEN REQUIRED** (Only If...)

You need a Hugging Face token **ONLY IF**:
1. Using **gated models** (requires approval, e.g., Llama 2, Gemma)
2. Using **private models** from your HF account
3. Want to **push models** to Hugging Face Hub
4. Exceed **rate limits** on public models (rare)

---

## 🔐 Where to Get Hugging Face Token

### Step 1: Create Hugging Face Account
- Go to https://huggingface.co
- Click "Sign Up" (free)

### Step 2: Generate Access Token
1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Choose token type:
   - **Read**: For downloading models (recommended)
   - **Write**: For uploading models
4. Name it: `organizational-ai`
5. Click "Generate token"
6. **Copy the token** (starts with `hf_...`)

### Step 3: Keep It Secret! 🔒
- Never commit tokens to Git
- Don't share in public
- Store in environment variables

---

## 📝 How to Configure Tokens

### Option 1: Local Development (.env file)

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env file:**
   ```bash
   # .env
   HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

3. **The app will auto-load it** (Python `dotenv` package)

### Option 2: Render Deployment

1. **Go to Render Dashboard**
   - Navigate to your service
   - Click "Environment" tab

2. **Add Environment Variable:**
   ```
   Key: HF_TOKEN
   Value: hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

3. **Save Changes**
   - Service will auto-redeploy

### Option 3: Hugging Face Spaces

1. **Go to your Space settings**
   - Click on your Space
   - Go to "Settings" tab

2. **Add Secret:**
   ```
   Name: HF_TOKEN
   Value: hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

3. **Visibility:** Set to "Private"

### Option 4: Docker/Self-Hosted

Pass as environment variable:
```bash
docker run -p 7860:7860 \
  -e HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \
  organizational-ai
```

---

## 🔧 Code Changes (If Using Token)

### For Gradio App

Update `gradio_app/app.py`:

```python
import os
from huggingface_hub import login

# Login to Hugging Face (if token provided)
hf_token = os.getenv("HF_TOKEN")
if hf_token:
    login(token=hf_token)
    print("✅ Logged into Hugging Face")
```

### For Inference Script

Update `hallucination_reduction/inference.py`:

```python
import os
from huggingface_hub import login

def load_model(model_name=BASE_MODEL, weights_dir=WEIGHTS_DIR):
    # Login if token available
    hf_token = os.getenv("HF_TOKEN")
    if hf_token:
        login(token=hf_token)
    
    print(f"Loading base model/tokenizer: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        token=hf_token  # Pass token explicitly
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        token=hf_token,  # Pass token explicitly
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",
    )
    # ... rest of code
```

### Install huggingface_hub

Add to `requirements.txt`:
```
huggingface-hub>=0.19.0
```

---

## 🎯 Quick Setup for Current Project

Since you're using **public models**, here's what you need:

### For Local Testing:
```bash
# No token needed! Just run:
python gradio_app/app.py
```

### For Render Deployment:
```bash
# No token needed! Just:
1. Push to GitHub
2. Connect to Render
3. Deploy
```

### For Hugging Face Spaces:
```bash
# No token needed for public models
# Token IS needed to create/manage Spaces
```

---

## 🔒 Security Best Practices

### ✅ DO:
- Store tokens in environment variables
- Use `.env` files locally (add to `.gitignore`)
- Use platform secrets (Render, HF Spaces)
- Rotate tokens periodically
- Use "Read" tokens when possible

### ❌ DON'T:
- Commit tokens to Git
- Share tokens publicly
- Use same token everywhere
- Store tokens in code files
- Post tokens in Discord/Slack

---

## 🚨 Token Leaked? Quick Fix!

1. **Revoke Immediately**
   - Go to https://huggingface.co/settings/tokens
   - Click "Revoke" on compromised token

2. **Generate New Token**
   - Create fresh token
   - Update all deployments

3. **Git History** (if committed)
   ```bash
   # Remove from Git history
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   
   # Force push (careful!)
   git push origin --force --all
   ```

4. **Change Immediately:**
   - All environment variables
   - All deployment secrets

---

## 📊 Token Usage Limits

### Free Tier (No Token):
- ✅ Download public models
- ✅ Use models for inference
- ⚠️ Rate limited (usually fine for small apps)

### With Token (Free Account):
- ✅ Higher rate limits
- ✅ Access gated models (with approval)
- ✅ Upload your own models
- ✅ Private repositories

### Pro Account ($9/month):
- ✅ Even higher limits
- ✅ Private Spaces
- ✅ GPU inference
- ✅ Priority support

---

## 🆘 Troubleshooting

### Error: "401 Unauthorized"
```
Solution: Add HF_TOKEN or model is private/gated
```

### Error: "429 Too Many Requests"
```
Solution: Add HF_TOKEN to increase rate limits
Or wait 1 hour for rate limit reset
```

### Error: "Model not found"
```
Solution: Check model name spelling
Or model requires access approval
```

### Token Not Working
```
Solution:
1. Check token starts with hf_
2. Verify token has "Read" permission
3. Regenerate token
4. Ensure token is in environment, not code
```

---

## 🎓 Summary

**For your current Organizational AI project:**

| Scenario | Token Needed? | Where to Add |
|----------|---------------|--------------|
| **Local testing** | ❌ No | N/A |
| **Render deploy** | ❌ No | N/A |
| **HF Spaces** | ❌ No (for inference) | N/A |
| **Gated models** | ✅ Yes | Environment variable |
| **Private models** | ✅ Yes | Environment variable |
| **Upload models** | ✅ Yes | Environment variable |

**Current Status:** ✅ **No token needed! Deploy away!**

---

## 📚 Additional Resources

- **HF Token Docs:** https://huggingface.co/docs/hub/security-tokens
- **Model Privacy:** https://huggingface.co/docs/hub/models-gated
- **Rate Limits:** https://huggingface.co/docs/hub/rate-limits
- **Environment Variables:** Check `.env.example` in repo

---

**Questions? Open an issue on GitHub!**
