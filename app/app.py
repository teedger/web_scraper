from flask import Flask, render_template, jsonify, send_file, Response, request
import threading
import queue
import datetime
import os
import sys
from io import StringIO
import json

app = Flask(__name__)

# Queue to capture print statements
output_queue = queue.Queue()
scraper_status = {"running": False, "completed": False, "file": None, "stopped": False}
stop_flag = threading.Event()

# News categories available for scraping
NEWS_CATEGORIES = {
    "Politics": "l/1",
    "Economics": "l/2",
    "Society": "l/3",
    "Health": "l/16",
    "World": "l/4",
    "Live_news": "t/58",
    "Technology": "l/7",
    "Mining": "l/20",
    "Bank_finance": "l/21",
    "Art": "l/6",
    "Business": "l/29",
    "Family": "l/23",
    "Geopolitics": "l/52",
    "Education": "l/11",
    "Sport": "l/5",
    "Ulaanbaatar": "l/53",
    "Crime": "l/12"
}


class OutputCapture:
    """Capture print statements and put them in a queue"""
    def __init__(self, queue):
        self.queue = queue
        self.terminal = sys.stdout

    def write(self, message):
        if message.strip():
            self.queue.put(message)
        self.terminal.write(message)

    def flush(self):
        self.terminal.flush()


def run_scraper(selected_categories):
    """Run the news scraper in a separate thread"""
    global scraper_status

    # Add parent directory to path to import scraper
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

    scraper_status["running"] = True
    scraper_status["completed"] = False
    scraper_status["stopped"] = False
    stop_flag.clear()

    # Capture output
    old_stdout = sys.stdout
    sys.stdout = OutputCapture(output_queue)

    try:
        output_queue.put("Starting Ikon news scraper...")
        output_queue.put(f"Selected categories: {', '.join(selected_categories)}")

        # Change to parent directory to run scraper
        original_dir = os.getcwd()
        os.chdir(parent_dir)

        # Custom scraper implementation with stop support
        import requests
        from bs4 import BeautifulSoup

        main_url = "https://ikon.mn/"
        n_list = []
        today = datetime.date.today().strftime("%Y%m%d")
        file_name = f"ikon_news_{today}.json"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Filter categories based on selection
        bulk_news_links = {k: v for k, v in NEWS_CATEGORIES.items() if k in selected_categories}

        news_id = 1
        for bulk_news in bulk_news_links:
            if stop_flag.is_set():
                output_queue.put("⚠️ Scraping stopped by user!")
                scraper_status["stopped"] = True
                break

            output_queue.put(f"Scraping all {bulk_news} news...")
            response = requests.get(main_url + bulk_news_links[bulk_news], headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Get list of page links
            main_page = soup.find("div", class_="ikblock")
            page_control = main_page.find("div", class_="ikpagination")
            total_pages = page_control.find(class_="ikp_items").find_all(class_="ikp_item")
            page_links = []
            for pages in total_pages:
                page_url = pages.get("data-url")
                if page_url:
                    page_link = f"https://ikon.mn/{page_url}"
                    page_links.append(page_link)

            for link in page_links:
                if stop_flag.is_set():
                    output_queue.put("⚠️ Scraping stopped by user!")
                    scraper_status["stopped"] = True
                    break

                response = requests.get(link, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")

                main_page = soup.find("div", class_="ikblock")
                news_container = main_page.find("div", class_="newslistcontainer")
                news_list = news_container.find_all("div", class_="nlitem") if news_container else []

                for news in news_list:
                    if stop_flag.is_set():
                        break

                    news_header = news.find("div", class_="nlheader").find("a").text.strip()
                    news_link_element = news.find("div", class_="nlheader").find("a")
                    news_link = f"https://ikon.mn/{news_link_element['href'].strip()}"
                    news_headline = news.find("div", class_="nlheadline").text.strip()
                    news_date = news.find("div", class_="tnldesc").find("div", class_="nldate")["rawdate"]
                    news_topic = bulk_news

                    news_dict = {
                        "news_id": str(news_id),
                        "news_topic": news_topic,
                        "news_header": news_header,
                        "news_headline": news_headline,
                        "news_date": news_date,
                        "news_link": news_link
                    }
                    n_list.append(news_dict)
                    news_id = news_id + 1

            # Save to JSON after each category
            with open(file_name, mode="w", encoding="utf-8") as json_file:
                json.dump(n_list, json_file, ensure_ascii=False, indent=4)

            output_queue.put(f"✅ Data saved to {file_name}")
            output_queue.put(f"Finished all {bulk_news} news.")

        if not scraper_status["stopped"]:
            scraper_status["file"] = file_name
            scraper_status["completed"] = True
            output_queue.put("Finished all news topics! The program will stop now.")
            output_queue.put(f"Scraping completed! File saved: {file_name}")
        else:
            # Still save partial results
            scraper_status["file"] = file_name
            output_queue.put(f"Partial results saved to: {file_name}")

    except Exception as e:
        output_queue.put(f"Error occurred: {str(e)}")
    finally:
        sys.stdout = old_stdout
        scraper_status["running"] = False
        # Change back to app directory
        try:
            os.chdir(original_dir)
        except:
            pass


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', categories=NEWS_CATEGORIES)


@app.route('/start', methods=['POST'])
def start_scraper():
    """Start the scraper"""
    if scraper_status["running"]:
        return jsonify({"status": "error", "message": "Scraper is already running"})

    # Get selected categories from request
    data = request.get_json()
    selected_categories = data.get('categories', list(NEWS_CATEGORIES.keys()))

    if not selected_categories:
        return jsonify({"status": "error", "message": "Please select at least one category"})

    # Clear previous status
    scraper_status["completed"] = False
    scraper_status["file"] = None
    scraper_status["stopped"] = False

    # Clear the queue
    while not output_queue.empty():
        output_queue.get()

    # Start scraper in a new thread
    thread = threading.Thread(target=run_scraper, args=(selected_categories,), daemon=True)
    thread.start()

    return jsonify({"status": "success", "message": "Scraper started"})


@app.route('/stop', methods=['POST'])
def stop_scraper():
    """Stop the running scraper"""
    if not scraper_status["running"]:
        return jsonify({"status": "error", "message": "No scraper is running"})

    stop_flag.set()
    output_queue.put("Stop request received...")

    return jsonify({"status": "success", "message": "Stopping scraper..."})


@app.route('/stream')
def stream():
    """Stream output to the frontend"""
    def generate():
        while True:
            try:
                message = output_queue.get(timeout=1)
                yield f"data: {json.dumps({'message': message})}\n\n"
            except queue.Empty:
                if not scraper_status["running"]:
                    if scraper_status["completed"] or scraper_status["stopped"]:
                        yield f"data: {json.dumps({'message': 'DONE', 'file': scraper_status['file']})}\n\n"
                        break
                continue

    return Response(generate(), mimetype='text/event-stream')


@app.route('/status')
def status():
    """Get current scraper status"""
    return jsonify(scraper_status)


@app.route('/download/<filename>')
def download(filename):
    """Download the generated file"""
    # Look for file in parent directory (where scraper runs)
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(parent_dir, filename)

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)
