# Railway Deployment Guide

Step-by-step guide to deploy the Ikon News Scraper to Railway.

## Prerequisites

✅ Railway account (done)
✅ Railway CLI installed (done)
✅ Project name: webcrawlerz (done)

## Deployment Steps

### Step 1: Navigate to the App Directory

```bash
cd /Users/user/Documents/Python/webCrawlerz/app
```

### Step 2: Login to Railway (if not already logged in)

```bash
railway login
```

This will open your browser for authentication.

### Step 3: Link to Your Project

```bash
railway link
```

When prompted:
1. Select **"Link to existing project"**
2. Choose **"webcrawlerz"** from the list

### Step 4: Create a .railwayignore File (Optional but Recommended)

This tells Railway what NOT to upload:

```bash
cat > .railwayignore << 'EOF'
*.csv
*.json
*.ndjson
__pycache__/
*.pyc
.DS_Store
.vscode/
.idea/
*.md
EOF
```

### Step 5: Deploy to Railway

```bash
railway up
```

This will:
- Upload your app files
- Install dependencies from requirements.txt
- Build and deploy your application

Wait for the deployment to complete (usually 1-3 minutes).

### Step 6: Generate a Public Domain

```bash
railway domain
```

This will generate a public URL like: `https://webcrawlerz-production.up.railway.app`

### Step 7: Open Your Deployed App

```bash
railway open
```

Or visit the URL shown in the previous step.

## Verification

After deployment, verify:

1. ✅ App loads in browser
2. ✅ Category selection works
3. ✅ Can start scraping
4. ✅ Console output appears
5. ✅ Can stop scraping
6. ✅ Can download results

## Viewing Logs

To see real-time logs:

```bash
railway logs
```

Or view logs in the Railway dashboard.

## Environment Variables (if needed)

If you need to add environment variables:

```bash
railway variables set KEY=VALUE
```

Or add them in the Railway dashboard under your project settings.

## Redeploying After Changes

After making code changes:

```bash
cd /Users/user/Documents/Python/webCrawlerz/app
railway up
```

Railway will automatically redeploy with your changes.

## Troubleshooting

### Issue: Port binding error
**Solution**: The app is configured to use Railway's PORT environment variable automatically.

### Issue: Module not found
**Solution**: Make sure the module is in requirements.txt and redeploy.

### Issue: App crashes on startup
**Solution**: Check logs with `railway logs` to see the error.

### Issue: Scraper fails in production
**Solution**: Some websites block cloud IPs. You may need to:
- Add retry logic
- Use proxy services
- Handle rate limiting

## Railway Dashboard

Access your dashboard at: https://railway.app/dashboard

Here you can:
- View deployment status
- Check logs
- Configure environment variables
- Set up custom domains
- Monitor resource usage

## Custom Domain (Optional)

To use your own domain:

1. Go to Railway dashboard
2. Select your project
3. Click "Settings" → "Domains"
4. Add your custom domain
5. Update DNS records as instructed

## Automatic Deployments from Git (Optional)

To enable automatic deployments:

1. Push your app to GitHub
2. In Railway dashboard, connect to GitHub repo
3. Enable automatic deployments
4. Every push to main branch will auto-deploy

## Cost

Railway offers:
- **Free tier**: $5 credit/month (enough for small projects)
- **Pro plan**: $20/month for more resources

Monitor your usage in the Railway dashboard.

## Important Notes

⚠️ **File Persistence**: Railway's filesystem is ephemeral. Downloaded files will be lost when the container restarts. For production, consider:
- Storing files in cloud storage (AWS S3, Google Cloud Storage)
- Using a database
- Returning files directly without saving

⚠️ **Memory Limits**: Free tier has memory limits. Large scraping jobs may fail.

⚠️ **Rate Limiting**: Be respectful of target websites. Add delays between requests.

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Railway Status: https://status.railway.app

## Quick Reference

```bash
# Deploy
railway up

# View logs
railway logs

# Open app
railway open

# Set environment variable
railway variables set KEY=VALUE

# Link to project
railway link

# Unlink project
railway unlink
```

---

**Your app is now live! 🎉**

Share your portfolio project: `https://your-app.up.railway.app`
