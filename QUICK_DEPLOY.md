# 🚀 Quick Deploy Guide

## Deploy to Render (5 minutes)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2: Deploy on Render
1. Go to [render.com](https://render.com) → Sign up/Login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `sustainability-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Click **"Add Environment Variable"**:
   - Key: `SECRET_KEY`
   - Value: Generate random string (or use: `python -c "import secrets; print(secrets.token_hex(32))"`)
6. Click **"Add PostgreSQL"**:
   - Name: `sustainability-db`
   - Plan: `Free`
7. Copy the **Internal Database URL** from PostgreSQL service
8. Go back to Web Service → Add Environment Variable:
   - Key: `DATABASE_URL`
   - Value: Paste the Internal Database URL
9. Click **"Create Web Service"**
10. Wait 5-10 minutes for deployment

✅ **Done!** Your app is live at: `https://sustainability-backend.onrender.com`

---

## Deploy to Railway (3 minutes)

### Step 1: Push to GitHub (same as above)

### Step 2: Deploy on Railway
1. Go to [railway.app](https://railway.app) → Sign up/Login
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Railway auto-detects Python and installs dependencies
5. Click **"+ New"** → **"Database"** → **"Add PostgreSQL"**
6. Railway automatically sets `DATABASE_URL`
7. Click on your service → **"Variables"** tab
8. Add:
   - `SECRET_KEY`: Generate random string
9. Railway auto-deploys!

✅ **Done!** Your app is live at: `https://your-app-name.up.railway.app`

---

## Generate Secret Key

Run this command to generate a secure secret key:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and use it as your `SECRET_KEY` environment variable.

---

## Test Your Deployment

After deployment, test your API:
```bash
curl https://your-app.onrender.com/api/foundational-principles
```

Visit admin UI:
```
https://your-app.onrender.com/admin
```

---

## Troubleshooting

**App won't start?**
- Check logs in hosting dashboard
- Verify `Procfile` exists: `web: gunicorn app:app`
- Check `requirements.txt` includes `gunicorn`

**Database errors?**
- Verify `DATABASE_URL` is set correctly
- Check PostgreSQL service is running
- Wait a few minutes after creating database

**502 Bad Gateway?**
- Render free tier spins down after 15 min inactivity
- First request takes 30-60 seconds to wake up
- This is normal for free tier

---

**Need help?** Check `DEPLOYMENT.md` for detailed instructions.

