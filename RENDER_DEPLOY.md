# 🚀 Quick Deploy to Render

Deploy Organizational AI to Render in under 5 minutes!

## Method 1: Blueprint (Automated - Recommended)

1. **Click the Deploy Button**
   
   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)
   
   Or manually:
   - Go to https://dashboard.render.com
   - Click "New +" → "Blueprint"

2. **Connect Repository**
   - Connect your GitHub account
   - Select: `Bishh-ui/Organizational_ai`
   - Render will detect `render.yaml`

3. **Configure**
   - Name: `organizational-ai` (or your choice)
   - Region: Select closest to you
   - Plan: **Free** (512MB RAM)

4. **Deploy**
   - Click "Apply"
   - Wait 5-10 minutes for first build
   - Model downloads happen during first deployment

5. **Access**
   - Your app URL: `https://organizational-ai.onrender.com`
   - Or check Render dashboard for your URL

## Method 2: Manual Setup

1. **Go to Render Dashboard**
   ```
   https://dashboard.render.com
   ```

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect GitHub: `Bishh-ui/Organizational_ai`

3. **Settings**
   ```
   Name: organizational-ai
   Region: Oregon (US West)
   Branch: main
   Root Directory: (leave empty)
   Runtime: Python 3
   Build Command: pip install -r gradio_app/requirements.txt
   Start Command: python gradio_app/app.py
   Instance Type: Free (512 MB RAM, 0.1 CPU)
   ```

4. **Environment Variables** (Advanced → Add Environment Variable)
   ```
   PORT=10000
   PYTHON_VERSION=3.10.0
   ADMIN_PIN=9999
   ```

5. **Create Web Service**
   - Click "Create Web Service"
   - Deployment starts automatically

## ⏱️ Deployment Timeline

- **Initial Deploy**: 5-10 minutes
  - Installing dependencies: ~3 min
  - Downloading models: ~5 min
  - First startup: ~1 min

- **Subsequent Deploys**: 2-3 minutes
  - Uses cached dependencies
  - Uses cached models

## 🎯 What Happens During Deployment

1. ✅ Render clones your GitHub repo
2. ✅ Installs Python dependencies from `requirements.txt`
3. ✅ Downloads AI models (TinyLlama, SentenceTransformers)
4. ✅ Starts Gradio app on port 10000
5. ✅ Provisions SSL certificate (HTTPS)
6. ✅ Assigns public URL

## 🔍 Checking Status

**View Logs:**
- Go to your service in Render dashboard
- Click "Logs" tab
- Look for: `Running on local URL:  http://0.0.0.0:10000`

**Successful Deployment Looks Like:**
```
Running on local URL:  http://0.0.0.0:10000
Running on public URL: https://organizational-ai.onrender.com

To create a public link, set `share=True` in `launch()`.
```

## ⚠️ Important Notes

### Free Tier Limitations
- **Spins down after 15 minutes** of inactivity
- **First request after sleep** takes 20-40 seconds (cold start)
- **750 hours/month** free (enough for 24/7 single app)
- **512MB RAM** (sufficient for TinyLlama, but tight)

### Performance Tips
1. **Keep Alive Service** (optional):
   - Use a service like UptimeRobot to ping your app every 14 minutes
   - Prevents spin-down
   - Free: https://uptimerobot.com

2. **Upgrade to Starter** ($7/month):
   - 2GB RAM (better performance)
   - No spin-down
   - Faster responses

### Troubleshooting

**Problem: Out of Memory Error**
```
Error: Process killed (out of memory)
```
**Solution:** 
- Upgrade to Starter plan (2GB RAM)
- Or use model quantization in code

**Problem: Slow First Request**
```
Taking 30+ seconds to respond
```
**Solution:**
- This is normal for cold starts (model loading)
- Consider Starter plan for always-on service
- Or use UptimeRobot to keep alive

**Problem: Build Failed**
```
Failed to install requirements
```
**Solution:**
- Check logs for specific error
- Ensure `gradio_app/requirements.txt` exists
- Verify Python version compatibility

## 🔒 Security Best Practices

Before going to production:

1. **Change Admin PIN**
   ```
   Environment Variable: ADMIN_PIN=your_secure_pin
   ```

2. **Add Rate Limiting**
   - Use Cloudflare (free)
   - Or implement in code

3. **Monitor Usage**
   - Check Render metrics
   - Set up alerts

## 📊 Monitoring

**Built-in Render Metrics:**
- Go to service → "Metrics" tab
- View CPU, Memory, Response time
- Free on all plans

**Custom Monitoring:**
- Add Sentry for error tracking
- Use Google Analytics for usage
- Implement custom logging

## 🎉 You're Live!

Once deployed:
- Share your URL: `https://organizational-ai.onrender.com`
- Test all features (Chat, Upload, Login, Admin)
- Monitor first few requests
- Consider adding to your resume/portfolio!

## 🆘 Need Help?

- **Render Docs**: https://render.com/docs
- **GitHub Issues**: https://github.com/Bishh-ui/Organizational_ai/issues
- **Render Community**: https://community.render.com

---

**Happy Deploying! 🚀**
