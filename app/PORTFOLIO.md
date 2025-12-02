# Ikon News Scraper - Portfolio Project

## Project Overview

A full-stack web application that scrapes news articles from ikon.mn (Mongolian news website) with real-time progress visualization.

## Key Features

### 🎯 Real-time Progress Tracking
- Live output streaming using Server-Sent Events (SSE)
- Terminal-style display shows scraping progress
- Status indicators (Idle, Running, Completed)

### 📥 One-Click Download
- Automatic file generation
- Download scraped data as JSON
- Date-stamped output files

### 🎨 Modern UI
- Gradient design with purple/blue theme
- Responsive layout
- Clean, professional interface
- Loading animations and status updates

### 🔧 Technical Implementation
- **Backend**: Flask web framework
- **Scraping**: BeautifulSoup4 + Requests
- **Concurrency**: Python threading
- **Real-time**: Server-Sent Events
- **Frontend**: Vanilla JavaScript, HTML5, CSS3

## Skills Demonstrated

### Backend Development
- Flask routing and blueprints
- RESTful API design
- Thread-safe operations
- Stream processing
- File handling and downloads

### Frontend Development
- EventSource API for SSE
- DOM manipulation
- Async JavaScript (Promises, Fetch API)
- CSS animations and transitions
- Responsive design

### Web Scraping
- HTML parsing with BeautifulSoup
- Pagination handling
- Data extraction and structuring
- Error handling and retries
- Ethical scraping practices

### Software Engineering
- Clean code architecture
- Separation of concerns
- Error handling
- User experience design
- Documentation

## Use Cases

1. **News Aggregation**: Collect news from multiple categories
2. **Data Analysis**: Gather data for trend analysis
3. **Content Monitoring**: Track news updates
4. **Research**: Academic or market research data collection

## Project Statistics

- **Categories Scraped**: 17 news categories
- **Languages**: Python, JavaScript, HTML, CSS
- **Dependencies**: Flask, BeautifulSoup4, Requests
- **Code Lines**: ~400 lines (app + scraper + frontend)

## Screenshots Description

### Landing Page
- Clean header with project title
- Information box explaining functionality
- Status indicator showing current state
- Start button with loading animation
- Terminal-style output window
- Modern gradient background

### Running State
- Animated spinner on button
- Real-time log output in terminal window
- Auto-scrolling to show latest messages
- Status changed to "Running..."

### Completion State
- Success message in terminal
- Download section appears
- Green download button
- Status shows "Completed"

## Technical Highlights

### Challenge: Real-time Output Streaming
**Solution**: Implemented custom OutputCapture class that intercepts print statements and queues them for SSE streaming to the frontend.

### Challenge: Non-blocking Scraper Execution
**Solution**: Used threading to run scraper in background while keeping web server responsive.

### Challenge: User Experience
**Solution**: Created terminal-style output window with auto-scroll and color coding for better visual feedback.

## Future Enhancements

- [ ] Data visualization dashboard
- [ ] Scheduled scraping (cron-like)
- [ ] Database integration
- [ ] Multi-user support
- [ ] Export to multiple formats (CSV, Excel)
- [ ] Filtering and search functionality

## Deployment Ready

This application can be deployed to:
- **Heroku**: With Gunicorn
- **AWS**: EC2 or Elastic Beanstalk
- **DigitalOcean**: Droplet with Nginx
- **Vercel/Netlify**: With serverless functions

## Links

- GitHub Repository: [Add your link]
- Live Demo: [Add your link]
- Documentation: See README.md

## Contact

For questions or collaboration: [Your contact info]

---

*This project demonstrates full-stack development capabilities, including web scraping, real-time communication, and modern web design.*
