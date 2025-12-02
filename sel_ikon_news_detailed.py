import os
import datetime
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Set today's date for file naming
today = datetime.date.today().strftime("%Y%m%d")

# File paths
source_file_name = f"ikon_news_20250508.json"
destination_file_name = f"ikon_news_detail_{today}.json"
checkpoint_file = "news_checkpoint.txt"

# Set up headless Chrome browser
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=chrome_options)

# Retry logic for HTTP requests
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount("http://", HTTPAdapter(max_retries=retries))
session.mount("https://", HTTPAdapter(max_retries=retries))

# Saving the progress and restarting from where left off
def get_last_processed_id():
    """Read the last processed ad_id from the checkpoint file."""
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, "r") as file:
            return file.read().strip()
    return None

def save_last_processed_id(news_id):
    """Save the last processed ad_id to the checkpoint file."""
    with open(checkpoint_file, "w") as file:
        file.write(news_id)


def safe_get_text(by, value):
    try:
        element = driver.find_element(by, value)
        return element.text.strip()
    except NoSuchElementException:
        return "N/A"

def news_info():
    # Get the last processed news_id
    last_processed_id = get_last_processed_id()
    resume = False if not last_processed_id else True

    news_data = []

    with open(source_file_name, mode="r", encoding="utf-8") as source_file:
        json_data = json.load(source_file)

        for idx, row in enumerate(json_data, start=1):
            link_text = row.get("news_link")
            news_id = row.get("news_id")
            news_header = row.get("news_header", "N/A")
            news_topic = row.get("news_topic", "N/A")

            if not link_text:
                print(f"Missing news_link in row {idx}. Skipping...")
                continue

            # Skip already processed rows
            if resume and news_id == last_processed_id:
                print(f"Resuming from row {idx + 1}...")
                resume = False  # Resume processing from the next row
                continue
            elif resume:
                continue

            print(f"Processing {idx}: {link_text}")

            try:
                driver.get(link_text)
                # Wait for the web page to finish loading
                time.sleep(1)

                # --- Extract Author ---
                try:
                    author_name = driver.find_element(By.CSS_SELECTOR, ".iauthor .name").text.strip()
                except NoSuchElementException:
                    author_name = "N/A"

                # --- Extract Reactions ---
                reaction_list = []
                try:
                    reaction_containers = driver.find_elements(By.CSS_SELECTOR, "#ikon_reaction_container .ikong__col")
                    reaction_labels = ["Love", "Haha", "Heart Eyes", "Wow", "Care", "Cry", "Poop", "Angry"]
                    for i, container in enumerate(reaction_containers):
                        try:
                            vote_id = container.find_element(By.CLASS_NAME, "vote").get_attribute("id").split("vote")[1]
                            value = container.find_element(By.CSS_SELECTOR, ".graph_inside .value").text.strip()
                        except NoSuchElementException:
                            value = "N/A"
                        if value != "N/A" and value != "":
                            reaction_list.append({
                                "reaction_type": reaction_labels[int(vote_id) - 1] if i < len(reaction_labels) else "Unknown",
                                "total_reactions": value
                            })
                except NoSuchElementException:
                    pass

                # --- Extract Comments ---
                comment_list = []
                try:
                    comments = driver.find_elements(By.CSS_SELECTOR, ".ikon-comment-container .ikoncomment")
                    for comment in comments:
                        try:
                            body = comment.find_element(By.CLASS_NAME, "ikoncbody")
                            comment_author = body.find_element(By.CLASS_NAME, "name").text.strip()
                            ip_address = body.find_element(By.CLASS_NAME, "ip").text.strip()
                            comment_text = body.find_element(By.CLASS_NAME, "comment").text.strip()
                            cvote = comment.find_element(By.CLASS_NAME, "cvote")
                            try:
                                vote_spans = cvote.find_elements(By.TAG_NAME, "span")
                                up_vote = vote_spans[0].text.strip() if len(vote_spans) >= 1 else "N/A"
                                down_vote = vote_spans[2].text.strip() if len(vote_spans) >= 3 else "N/A"
                            except Exception:
                                up_vote = "N/A"
                                down_vote = "N/A"

                            comment_list.append({
                                "Author": comment_author,
                                "IP Address": ip_address,
                                "Comment": comment_text,
                                "Total up vote": up_vote,
                                "Total down vote": down_vote
                            })
                        except Exception:
                            continue
                except NoSuchElementException:
                    pass

                # --- Save data ---
                news_dict = {
                    "id": news_id,
                    "news_topic": news_topic,
                    "news_header": news_header,
                    "news_author": author_name,
                    "reactions": reaction_list,
                    "comments": comment_list
                }
                news_data.append(news_dict)

                # Save progress
                save_last_processed_id(news_id)

            except Exception as e:
                print(f"Error processing {link_text}: {e}")

            # Dump all collected data to JSON
            with open(destination_file_name, mode="w", encoding="utf-8") as file:
                json.dump(news_data, file, ensure_ascii=False, indent=4)

    print(f"✅ Data finished saving to {destination_file_name}")
    if os.path.exists("news_checkpoint.txt"):
        os.remove("news_checkpoint.txt")
        print("Deleted checkpoint file")
    else:
        print("Checkpoint file does not exist!")

if __name__ == "__main__":
    try:
        news_info()
    finally:
        driver.quit()
