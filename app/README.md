# Ikon News Scraper Web Application

A simple Flask-based web application that scrapes news articles from ikon.mn (a Mongolian news website) and displays live progress in the browser.

## Features

- **Real-time Progress**: Watch the scraping progress live in your browser
- **Download Results**: Download the scraped data as a JSON file
- **Clean UI**: Simple, modern interface with gradient design
- **Multiple Categories**: Scrapes from 17 different news categories including Politics, Economics, Society, Health, World, Technology, and more

## Project Structure

```
webCrawlerz/
├── app/                        # Web application folder
│   ├── app.py                  # Flask web application
│   ├── run.sh                  # Startup script
│   ├── templates/
│   │   └── index.html          # Web interface
│   ├── README.md               # This file
│   ├── QUICKSTART.md           # Quick start guide
│   └── PORTFOLIO.md            # Portfolio documentation
├── bs_ikon_news.py             # News scraper script (parent dir)
├── requirements.txt            # Python dependencies (parent dir)
└── [other scraper scripts]
```

## How It Works

### Backend (app.py)

The Flask application consists of several key components:

1. **OutputCapture Class**: Captures print statements from the scraper and puts them in a queue for real-time streaming to the frontend.

2. **run_scraper()**: Runs the news scraper in a separate thread to prevent blocking the web server.

3. **Routes**:
   - `/` - Main page that displays the web interface
   - `/start` - POST endpoint that starts the scraper
   - `/stream` - Server-Sent Events (SSE) endpoint that streams live output
   - `/status` - Returns current scraper status (running/completed)
   - `/download/<filename>` - Downloads the generated JSON file

### Frontend (index.html)

The web interface provides:

- A start button to begin scraping
- A terminal-style output window that displays live progress
- Status indicators (Idle, Running, Completed)
- A download button that appears when scraping is complete
- Responsive design with modern styling

### Scraper (bs_ikon_news.py)

The scraper uses BeautifulSoup to:

1. Iterate through 17 news categories
2. For each category, find all pagination pages
3. Extract article data from each page:
   - News ID
   - Topic/Category
   - Header/Title
   - Headline/Description
   - Publication date
   - Article link
4. Save all data to a JSON file with the current date

## Installation

1. Clone or download this project

2. Navigate to the app directory:
```bash
cd webCrawlerz/app
```

3. Install dependencies (from parent directory):
```bash
pip3 install --user -r ../requirements.txt
```

## Usage

1. Start the Flask server from the app directory:
```bash
cd app
./run.sh
```

Or run directly:
```bash
cd app
python3 app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Click "Start Scraping" button

4. Watch the live progress in the terminal window

5. When complete, click "Download JSON File" to get your data

## Output Format

The scraper generates a JSON file named `ikon_news_YYYYMMDD.json` with the following structure:

```json
[
    {
        "news_id": "1",
        "news_topic": "Politics",
        "news_header": "Article Title",
        "news_headline": "Article description or summary",
        "news_date": "2024-01-01T12:00:00",
        "news_link": "https://ikon.mn/..."
    },
    ...
]
```

## Technologies Used

- **Flask**: Lightweight web framework for Python
- **BeautifulSoup4**: HTML parsing and web scraping
- **Requests**: HTTP library for making web requests
- **Server-Sent Events (SSE)**: Real-time communication from server to client
- **Threading**: Concurrent execution of scraper and web server

## How the Real-time Streaming Works

1. When you click "Start Scraping", the frontend sends a POST request to `/start`
2. The backend starts the scraper in a new thread
3. The frontend opens an EventSource connection to `/stream`
4. As the scraper runs, print statements are captured and queued
5. The `/stream` endpoint yields these messages to the frontend in real-time
6. The frontend displays each message in the terminal window
7. When complete, a download button appears

## Portfolio Presentation

This project demonstrates:

- **Full-stack development**: Backend (Flask) + Frontend (HTML/CSS/JS)
- **Asynchronous programming**: Threading and real-time data streaming
- **Web scraping**: Data extraction from websites
- **User experience**: Live feedback and progress updates
- **Clean code**: Organized structure with clear separation of concerns

## Limitations

- Scraper runs sequentially (not parallelized)
- Only one scraping session can run at a time
- No data persistence (files are saved locally)
- No authentication or user management

## Future Enhancements

- Add data visualization of scraped articles
- Implement scheduling (run scraper at specific times)
- Add database storage (SQLite/PostgreSQL)
- Create multiple scraper configurations
- Add export formats (CSV, Excel)
- Implement scraper history and statistics

## License

Free to use for educational and portfolio purposes.

## Notes

This scraper is designed for educational purposes. Always respect website terms of service and robots.txt when scraping.
