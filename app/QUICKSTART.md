# Quick Start Guide

Get the Ikon News Scraper running in 3 easy steps!

## Step 1: Navigate to App Directory

```bash
cd webCrawlerz/app
```

## Step 2: Install Dependencies

From the app directory:

```bash
pip3 install --user -r ../requirements.txt
```

Or if you prefer using a virtual environment:

```bash
cd ..
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd app
```

## Step 3: Run the Application

**Option A - Using the run script (easiest):**
```bash
./run.sh
```

**Option B - Direct Python:**
```bash
python3 app.py
```

## Step 4: Open in Browser

Navigate to: **http://localhost:5000**

## Using the Application

1. Click the **"Start Scraping"** button
2. Watch the live progress in the terminal window
3. When complete, click **"Download JSON File"**
4. Your scraped news data will be downloaded!

## What Gets Scraped?

The scraper collects news from these categories on ikon.mn:
- Politics
- Economics
- Society
- Health
- World
- Technology
- Mining
- Bank & Finance
- Art
- Business
- Family
- Geopolitics
- Education
- Sport
- Ulaanbaatar
- Crime

## Troubleshooting

**Port already in use?**
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

**Flask not found?**
```bash
pip3 install --user Flask==3.0.0
```

**Permission denied on run.sh?**
```bash
chmod +x run.sh
```

## Output

The scraper creates a JSON file named: `ikon_news_YYYYMMDD.json`

Each article contains:
- news_id
- news_topic (category)
- news_header (title)
- news_headline (description)
- news_date
- news_link

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## For Your Portfolio

This project showcases:
- Web scraping with BeautifulSoup
- Real-time web application with Flask
- Server-Sent Events for live updates
- Threading for concurrent operations
- Clean, modern UI design
- Full-stack development skills

Enjoy scraping! 🚀
