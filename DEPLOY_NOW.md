# 🚀 Deploy Your App Now - Step by Step

Your code is ready! Follow these exact steps to deploy to Render (free):

## ✅ Pre-Deployment Checklist

Your code is already on GitHub at: `https://github.com/RidheeshAmarthya/S_Backend`

All required files are present:
- ✅ `Procfile` ✓
- ✅ `requirements.txt` ✓
- ✅ `runtime.txt` ✓
- ✅ `app.py` configured for production ✓

---

## 🎯 Deploy to Render (5 minutes)

### Step 1: Sign Up / Login to Render
1. Go to: **https://render.com**
2. Click **"Get Started for Free"** or **"Sign In"**
3. Sign up with GitHub (recommended - easier connection)

### Step 2: Create PostgreSQL Database
1. Click **"New +"** button (top right)
2. Select **"PostgreSQL"**
3. Configure:
   - **Name**: `sustainability-db`
   - **Database**: `sustainability` (or leave default)
   - **User**: `sustainability_user` (or leave default)
   - **Region**: Choose closest to you
   - **Plan**: **Free**
4. Click **"Create Database"**
5. **Wait 2-3 minutes** for database to be created
6. Once created, click on the database
7. Go to **"Connections"** tab
8. Copy the **"Internal Database URL"** (looks like: `postgresql://user:pass@host:5432/dbname`)
   - ⚠️ **Save this URL** - you'll need it in Step 3

### Step 3: Create Web Service
1. Click **"New +"** button again
2. Select **"Web Service"**
3. Click **"Connect account"** next to GitHub (if not connected)
4. Authorize Render to access your GitHub
5. Find and select repository: **`RidheeshAmarthya/S_Backend`**
6. Click **"Connect"**

### Step 4: Configure Web Service
Fill in these settings:

**Basic Settings:**
- **Name**: `sustainability-backend` (or any name you like)
- **Region**: Same as database
- **Branch**: `main`
- **Root Directory**: (leave empty)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

**Environment Variables:**
Click **"Add Environment Variable"** and add:

1. **SECRET_KEY**:
   - Key: `SECRET_KEY`
   - Value: Generate one by running this in terminal:
     ```bash
     python3 -c "import secrets; print(secrets.token_hex(32))"
     ```
   - Or use: `your-super-secret-key-change-this-12345`

2. **DATABASE_URL**:
   - Key: `DATABASE_URL`
   - Value: Paste the **Internal Database URL** you copied from Step 2

3. **FLASK_ENV** (optional):
   - Key: `FLASK_ENV`
   - Value: `production`

### Step 5: Deploy!
1. Scroll down and click **"Create Web Service"**
2. Wait 5-10 minutes for first deployment
3. Watch the build logs - you'll see:
   - Installing dependencies
   - Building application
   - Starting server

### Step 6: Test Your Deployment
Once deployment completes (green checkmark):

1. **Get your app URL**: It will be something like:
   - `https://sustainability-backend.onrender.com`

2. **Test API**:
   ```bash
   curl https://sustainability-backend.onrender.com/api/foundational-principles
   ```

3. **Access Admin UI**:
   - Visit: `https://sustainability-backend.onrender.com/admin`
   - You should see the dashboard!

---

## 🎉 Success!

Your app is now live! 

**Important Notes:**
- ⚠️ Free tier spins down after 15 min inactivity
- First request after spin-down takes 30-60 seconds
- Database is automatically initialized on first request
- File uploads work but are ephemeral (lost on restart)

---

## 🔧 Troubleshooting

### Build Fails?
- Check build logs in Render dashboard
- Verify `requirements.txt` is correct
- Make sure Python version matches `runtime.txt`

### Database Connection Error?
- Verify `DATABASE_URL` is set correctly
- Check database is running (green status)
- Wait a few minutes after creating database

### App Won't Start?
- Check logs for errors
- Verify `Procfile` exists: `web: gunicorn app:app`
- Make sure `gunicorn` is in `requirements.txt`

### 502 Bad Gateway?
- Normal for free tier - app is spinning up
- Wait 30-60 seconds and refresh
- Check logs for any errors

---

## 📞 Need Help?

If you encounter issues:
1. Check the build/deploy logs in Render dashboard
2. Verify all environment variables are set
3. Make sure database is running
4. Check that all files are committed to GitHub

---

**Your app URL will be**: `https://[your-service-name].onrender.com`

Good luck! 🚀

