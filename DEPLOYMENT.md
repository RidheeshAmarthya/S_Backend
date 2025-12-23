# Free Hosting Deployment Guide

This guide covers deploying the Sustainability Backend to free hosting platforms.

## 🚀 Best Free Hosting Options

### 1. **Render** (Recommended - Easiest)
- ✅ Free PostgreSQL database
- ✅ Free SSL certificate
- ✅ Auto-deploy from GitHub
- ✅ 750 hours/month free (enough for 24/7)
- ⚠️ Spins down after 15 min inactivity (freezes on first request)

**Steps:**
1. Push your code to GitHub
2. Go to [render.com](https://render.com) and sign up
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: sustainability-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Add Environment Variables:
   - `SECRET_KEY`: Generate a random string (or use Render's auto-generate)
7. Add PostgreSQL Database:
   - Click "New +" → "PostgreSQL"
   - Name it "sustainability-db"
   - Copy the "Internal Database URL"
   - Add as environment variable `DATABASE_URL` in your web service
8. Click "Create Web Service"
9. Wait for deployment (5-10 minutes)

**Your app will be live at**: `https://sustainability-backend.onrender.com`

---

### 2. **Railway** (Great Alternative)
- ✅ $5 free credit monthly
- ✅ PostgreSQL included
- ✅ No spin-down (stays active)
- ⚠️ Credit runs out eventually (but generous)

**Steps:**
1. Push code to GitHub
2. Go to [railway.app](https://railway.app) and sign up
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Python and installs dependencies
6. Add PostgreSQL:
   - Click "+ New" → "Database" → "Add PostgreSQL"
   - Railway automatically sets `DATABASE_URL`
7. Add Environment Variable:
   - `SECRET_KEY`: Generate random string
8. Deploy automatically starts

**Your app will be live at**: `https://your-app-name.up.railway.app`

---

### 3. **Fly.io** (Good for Global)
- ✅ Free tier available
- ✅ Global edge network
- ⚠️ Requires CLI setup

**Steps:**
1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Sign up: `fly auth signup`
3. Create app: `fly launch`
4. Add PostgreSQL: `fly postgres create`
5. Set secrets: `fly secrets set SECRET_KEY=your-secret-key`
6. Deploy: `fly deploy`

---

### 4. **PythonAnywhere** (Simple but Limited)
- ✅ Free tier available
- ⚠️ Limited to 1 web app
- ⚠️ Uses SQLite (not PostgreSQL)

**Steps:**
1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your files via Files tab
3. Create web app in Web tab
4. Configure WSGI file
5. Reload web app

---

## 📋 Pre-Deployment Checklist

Before deploying, make sure:

- [x] Code is pushed to GitHub
- [x] `requirements.txt` includes all dependencies
- [x] `Procfile` exists (for Render/Railway)
- [x] `SECRET_KEY` is set as environment variable
- [x] Database URL is configured (PostgreSQL for production)
- [x] `.gitignore` excludes database files and uploads

## 🔧 Environment Variables

Set these in your hosting platform:

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key (required) | `your-random-secret-key-here` |
| `DATABASE_URL` | PostgreSQL connection string | Auto-set by Render/Railway |
| `PORT` | Server port | Auto-set by platform |
| `FLASK_ENV` | Environment mode | `production` |

## 🗄️ Database Migration

The app automatically creates tables on first run. For production:

1. **Render/Railway**: PostgreSQL is automatically connected via `DATABASE_URL`
2. **First deployment**: Tables are created automatically
3. **Sample data**: Loaded via `init_data.py` on first run

## 📁 File Uploads

**Important**: Free hosting platforms have ephemeral file systems. Uploads will be lost on restart.

**Solutions:**
1. **Use cloud storage** (recommended):
   - AWS S3 (free tier: 5GB)
   - Cloudinary (free tier: 25GB)
   - Uploadcare (free tier available)

2. **Use database** for small files (base64 encoding)

3. **Accept loss** for development/testing

## 🔗 Post-Deployment

After deployment:

1. **Test your API**: 
   ```bash
   curl https://your-app.onrender.com/api/foundational-principles
   ```

2. **Access Admin UI**: 
   Visit `https://your-app.onrender.com/admin`

3. **Initialize Database** (if needed):
   - First request automatically initializes
   - Or manually trigger via admin UI

## 🐛 Troubleshooting

### App won't start
- Check logs in hosting dashboard
- Verify `Procfile` exists
- Check `requirements.txt` is correct

### Database errors
- Verify `DATABASE_URL` is set
- Check PostgreSQL is running
- Review connection string format

### 502 Bad Gateway
- App might be spinning up (Render free tier)
- Wait 30 seconds and retry
- Check application logs

### Uploads not working
- File system is ephemeral
- Consider cloud storage solution

## 📚 Additional Resources

- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Fly.io Docs](https://fly.io/docs)

---

**Recommended**: Start with **Render** - it's the easiest and most beginner-friendly option!

