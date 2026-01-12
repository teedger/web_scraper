# Quick Deployment Checklist

Follow these steps in order:

## 1. Navigate to App Directory
```bash
cd /Users/user/Documents/Python/webCrawlerz/app
```

## 2. Login to Railway
```bash
railway login
```

## 3. Link to Your Project
```bash
railway link
```
- Select: **Link to existing project**
- Choose: **webcrawlerz**

## 4. Deploy
```bash
railway up
```
Wait for deployment to complete (~2-3 minutes)

## 5. Generate Public URL
```bash
railway domain
```
Copy the generated URL (e.g., `https://webcrawlerz-production.up.railway.app`)

## 6. Test Your App
```bash
railway open
```
Or visit the URL from step 5

## 7. Verify Everything Works
- [ ] App loads
- [ ] Can select categories
- [ ] Can start scraping
- [ ] Console output appears
- [ ] Can stop scraping
- [ ] Can download files

## Done! 🎉

Your app is live at: `https://your-url.up.railway.app`

---

## Need Help?

View logs:
```bash
railway logs
```

Redeploy after changes:
```bash
railway up
```

View in dashboard:
```bash
railway open
```
