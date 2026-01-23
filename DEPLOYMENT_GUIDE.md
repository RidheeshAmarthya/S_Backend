# Quick Deployment Guides

## 🚀 Render (Recommended - Easiest)

### Step 1: Prepare Your Code
1. Make sure your code is pushed to GitHub
2. All files are ready (Procfile, requirements.txt, etc.)

### Step 2: Deploy on Render
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: sustainability-backend (or your choice)
   - **Region**: Choose closest to you
   - **Branch**: main (or your default branch)
   - **Root Directory**: (leave empty)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Click "Advanced" and add Environment Variables:
   - `SECRET_KEY`: Generate a random string (use: `python -c "import secrets; print(secrets.token_hex(32))"`)
   - `FLASK_ENV`: `production`
6. Click "Create Web Service"

### Step 3: Add PostgreSQL Database (Optional but Recommended)
1. In Render dashboard, click "New +" → "PostgreSQL"
2. Configure and create
3. Copy the "Internal Database URL"
4. Go back to your Web Service → Environment
5. Add: `DATABASE_URL` = (paste the Internal Database URL)

### Step 4: Deploy
- Render will automatically deploy
- Wait for build to complete
- Your app will be live at: `https://your-app-name.onrender.com`

---

## 🚂 Railway

### Step 1: Deploy
1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Python and Flask
5. Add Environment Variables:
   - `SECRET_KEY`: (generate random string)
   - `PORT`: Railway sets this automatically
6. Click "Deploy"

### Step 2: Add PostgreSQL
1. Click "New" → "Database" → "Add PostgreSQL"
2. Railway automatically sets `DATABASE_URL` environment variable
3. Your app will automatically reconnect

### Step 3: Get Your URL
- Railway provides a URL like: `https://your-app.up.railway.app`
- You can add a custom domain later

---

## 🐳 Docker Deployment

### Local Testing
```bash
# Build the image
docker build -t sustainability-backend .

# Run the container
docker run -p 5003:5003 \
  -e SECRET_KEY=your-secret-key \
  -v $(pwd)/uploads:/app/uploads \
  sustainability-backend
```

### Using Docker Compose
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Deploy Docker to:
- **Fly.io**: `flyctl launch` (reads Dockerfile)
- **Google Cloud Run**: Upload container to GCR
- **AWS ECS/Fargate**: Push to ECR
- **DigitalOcean App Platform**: Auto-detects Dockerfile

---

## ☁️ DigitalOcean App Platform

1. Go to [cloud.digitalocean.com](https://cloud.digitalocean.com)
2. Create → App Platform
3. Connect GitHub repository
4. Auto-detects Python/Flask
5. Configure:
   - Build command: `pip install -r requirements.txt`
   - Run command: `gunicorn app:app`
6. Add environment variables
7. Add managed PostgreSQL database
8. Deploy

**Cost**: ~$5-12/month

---

## 🔧 Post-Deployment Checklist

- [ ] Test API endpoints: `https://your-app.com/api/foundational-principles`
- [ ] Test Admin UI: `https://your-app.com/admin`
- [ ] Verify database is working (create a test entry)
- [ ] Check file uploads work (if using cloud storage)
- [ ] Set up custom domain (optional)
- [ ] Configure CORS for your frontend domain
- [ ] Set up monitoring/logging
- [ ] Enable automatic backups (if using managed database)

---

## 🔐 Security Notes

1. **Never commit** `.env` files or `SECRET_KEY` to Git
2. Use strong `SECRET_KEY` in production
3. Limit CORS to your frontend domain:
   ```python
   CORS(app, resources={r"/api/*": {"origins": "https://your-frontend.com"}})
   ```
4. Use HTTPS (most platforms provide this automatically)
5. Consider rate limiting for API endpoints
6. Use environment variables for all secrets

---

## 📊 Monitoring Options

- **Render**: Built-in logs and metrics
- **Railway**: Built-in logs
- **Sentry**: Error tracking (add to requirements.txt)
- **Uptime Robot**: Free uptime monitoring

---

## 💡 Tips

- Start with Render or Railway for easiest deployment
- Use PostgreSQL in production (not SQLite)
- Use cloud storage (S3, Cloudinary) for file uploads in production
- Set up CI/CD for automatic deployments
- Use environment variables for all configuration

Need help with a specific platform? Let me know!
