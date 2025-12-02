# Web Scraper Collection

A collection of Python web scraping scripts for Mongolian websites.

## 📁 Project Structure

```
webCrawlerz/
├── app/                          # 🌐 Flask Web Application (Portfolio Project)
│   ├── app.py
│   ├── run.sh
│   ├── templates/
│   ├── README.md
│   ├── QUICKSTART.md
│   └── PORTFOLIO.md
├── bs_ikon_news.py               # Ikon.mn news scraper
├── bs_unegui_car.py              # Unegui.mn car listings scraper
├── bs_unegui_property.py         # Unegui.mn property scraper
├── bs_zangia_company.py          # Zangia.mn company scraper
├── bs_zangia_jobs.py             # Zangia.mn job listings scraper
├── bs_1234_lessons.py            # 1234.mn lessons scraper
└── requirements.txt              # Python dependencies
```

## 🚀 Quick Start

### Web Application (Portfolio Project)

Run the interactive web interface for the Ikon news scraper:

```bash
cd app
./run.sh
```

Then open: http://localhost:5000

See **app/README.md** for full documentation.

### Individual Scrapers

Run any scraper directly:

```bash
python3 bs_ikon_news.py
python3 bs_unegui_property.py
python3 bs_zangia_jobs.py
```

## 📦 Installation

Install all dependencies:

```bash
pip3 install --user -r requirements.txt
```

## 🎯 Features

### Web Application (`app/`)
- Real-time progress tracking
- Terminal-style output display
- One-click file download
- Modern, responsive UI
- Server-Sent Events for live updates

### Scrapers
- **Ikon News**: Scrapes 17 news categories from ikon.mn
- **Unegui Cars**: Collects car listings with prices and details
- **Unegui Property**: Gathers property/real estate listings
- **Zangia Jobs**: Extracts job postings
- **Zangia Companies**: Collects company information
- **1234 Lessons**: Scrapes educational content

## 🛠 Technologies

- **Web Scraping**: BeautifulSoup4, Selenium, Requests
- **Web Framework**: Flask
- **Data Storage**: JSON, CSV
- **Real-time**: Server-Sent Events (SSE)
- **Concurrency**: Threading, tqdm progress bars

## 📝 Output Formats

Scrapers generate timestamped output files:
- `ikon_news_YYYYMMDD.json`
- `car_list_YYYYMMDD.csv`
- `property_list_YYYYMMDD.csv`
- `job_list_YYYYMMDD.csv`
- etc.

## 🌟 Portfolio Highlight

The **app/** folder contains a full-stack web application perfect for portfolio demonstrations. It showcases:
- Backend development (Flask)
- Frontend development (HTML/CSS/JavaScript)
- Real-time communication
- Web scraping integration
- Clean, modern UI/UX

See **app/PORTFOLIO.md** for detailed project description.

## 📚 Documentation

- **app/README.md** - Web application documentation
- **app/QUICKSTART.md** - Quick start guide
- **app/PORTFOLIO.md** - Portfolio presentation

## ⚠️ Notes

- These scrapers are for educational purposes
- Respect website terms of service and robots.txt
- Use appropriate delays between requests
- Some scrapers may need updates if websites change structure

## 📄 License

Free to use for educational and portfolio purposes.
