# Deployment Guide for Organizational AI

This guide covers deployment options for the Organizational AI web application.

---

## 🚀 Render Deployment (Recommended - Free Tier Available)

Render provides free hosting with 512MB RAM and automatic deployments from GitHub.

### Prerequisites
- GitHub account with your code pushed
- Render account (sign up at https://render.com)

### Step-by-Step Instructions

#### Option 1: Using render.yaml (Automated)

1. **Push your code to GitHub** (already done ✅)
   ```bash
   git push origin main
   ```

2. **Go to Render Dashboard**
   - Visit https://dashboard.render.com
   - Click "New +" → "Blueprint"

3. **Connect Repository**
   - Connect your GitHub account
   - Select repository: `Bishh-ui/Organizational_ai`
   - Render will automatically detect `render.yaml`

4. **Deploy**
   - Click "Apply"
   - Render will build and deploy automatically
   - Wait 5-10 minutes for first deployment (downloads models)

5. **Access Your App**
   - Your app will be at: `https://organizational-ai.onrender.com`
   - Or the URL shown in your Render dashboard

#### Option 2: Manual Setup

1. **Create New Web Service**
   - Go to https://dashboard.render.com
   - Click "New +" → "Web Service"

2. **Connect Repository**
   - Connect GitHub and select `Bishh-ui/Organizational_ai`

3. **Configure Service**
   ```
   Name: organizational-ai
   Region: Oregon (or closest to you)
   Branch: main
   Root Directory: (leave blank)
   Runtime: Python 3
   Build Command: pip install -r gradio_app/requirements.txt
   Start Command: python gradio_app/app.py
   ```

4. **Set Environment Variables**
   - Click "Advanced" → "Add Environment Variable"
   ```
   PORT = 10000
   PYTHON_VERSION = 3.10.0
   ADMIN_PIN = 9999
   ```

5. **Choose Plan**
   - Select "Free" plan (512MB RAM, enough for the app)

6. **Create Web Service**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)

### Important Notes for Render

**Free Tier Limitations:**
- ✅ 512MB RAM (sufficient for TinyLlama)
- ✅ Automatic SSL certificate
- ✅ Continuous deployment from Git
- ⚠️ Spins down after 15 minutes of inactivity (first request takes ~30s to wake)
- ⚠️ 750 hours/month free (roughly 1 app running 24/7)

**Performance Tips:**
- First request after sleep takes 20-40 seconds (model loading)
- Subsequent requests are fast (~2-3 seconds)
- Consider upgrading to Starter ($7/month) for always-on service

**Troubleshooting:**
- If deployment fails with "Out of Memory", the model is too large for free tier
- Solution: Upgrade to Starter plan with 2GB RAM
- Alternative: Use smaller model or model quantization

---

## ☁️ Hugging Face Spaces (Alternative - Free GPU Available)

Perfect for ML applications with free GPU access.

### Quick Deploy

1. **Create Space**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose:
     - Name: organizational-ai
     - SDK: Gradio
     - Hardware: CPU Basic (free) or upgrade to GPU

2. **Upload Files**
   - Upload contents of `gradio_app/` folder
   - Or clone and push via Git:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/organizational-ai
   cp -r gradio_app/* organizational-ai/
   cd organizational-ai
   git add .
   git commit -m "Initial deployment"
   git push
   ```

3. **Configure**
   - Spaces will auto-detect `app.py` and `requirements.txt`
   - Set secrets in Space settings:
     - `ADMIN_PIN` = 9999

4. **Deploy**
   - Deployment is automatic
   - App will be at: `https://huggingface.co/spaces/YOUR_USERNAME/organizational-ai`

### Hugging Face Advantages
- ✅ Free GPU option (T4 GPU for $0.60/hour)
- ✅ Built-in model caching
- ✅ Great for ML workloads
- ✅ Community features (likes, comments)

---

## 🐳 Docker Deployment (Self-Hosted)

For deploying on your own server or cloud provider.

### Using Docker

1. **Build Image**
   ```bash
   docker build -t organizational-ai .
   ```

2. **Run Container**
   ```bash
   docker run -p 7860:7860 \
     -e ADMIN_PIN=9999 \
     organizational-ai
   ```

3. **Access**
   - Local: http://localhost:7860
   - Server: http://your-server-ip:7860

---

## 🌐 Other Deployment Options

### Railway
- Similar to Render, free tier available
- https://railway.app

### Vercel
- ❌ Not recommended - serverless functions have 10s timeout
- Too short for model inference

### AWS/GCP/Azure
- Use EC2, Cloud Run, or App Service
- More complex but full control
- Recommended for production with high traffic

---

## 📊 Resource Requirements

| Component | RAM | Storage | Notes |
|-----------|-----|---------|-------|
| TinyLlama Model | ~2GB | ~2.5GB | Loaded into RAM |
| Sentence Transformers | ~500MB | ~500MB | For retrieval |
| Gradio App | ~200MB | ~100MB | Python dependencies |
| **Total** | **~3GB** | **~3GB** | Minimum requirements |

**Recommendations:**
- **Development**: Free tier (Render/HF Spaces)
- **Production**: Starter tier with 2-4GB RAM
- **High Traffic**: Dedicated server with 8GB+ RAM

---

## 🔒 Security Notes

Before deploying to production:

1. **Change Admin PIN**
   - Set `ADMIN_PIN` environment variable
   - Don't use default "9999"

2. **Add Authentication**
   - Consider adding OAuth or JWT auth
   - Restrict access to internal network if needed

3. **Rate Limiting**
   - Add rate limiting to prevent abuse
   - Use services like Cloudflare

4. **HTTPS**
   - Render/HF Spaces provide free SSL
   - For self-hosted, use Let's Encrypt

---

## 📈 Monitoring

### Render
- Built-in logs and metrics
- View in dashboard under "Logs" tab

### Hugging Face
- View logs in Space settings
- Monitor community engagement

### Self-Hosted
- Use tools like:
  - Grafana for metrics
  - Sentry for error tracking
  - CloudWatch/DataDog for cloud

---

## 🆘 Getting Help

- **Render Docs**: https://render.com/docs
- **Hugging Face Docs**: https://huggingface.co/docs/hub/spaces
- **GitHub Issues**: https://github.com/Bishh-ui/Organizational_ai/issues

---

**Need help? Open an issue on GitHub!**
