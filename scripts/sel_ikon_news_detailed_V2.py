#!/usr/bin/env python3
"""
Scrape ikon.mn news details → NDJSON.

Features
--------
* Crash-safe resume (checkpoint file)
* One-line-per-record NDJSON output (no big rewrites)
* Selenium waits with explicit WebDriverWait
"""

import os
import json
import datetime
from contextlib import suppress
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
)

# ───────────────────────────────
# 1.  Config & filenames
# ───────────────────────────────
TODAY = datetime.date.today().strftime("%Y%m%d")
SOURCE_FILE = f"../output/ikon_news_{TODAY}.json"
DEST_FILE = f"../output/ikon_news_detail_{TODAY}.ndjson"   # NDJSON ➜ .ndjson
CHECKPOINT_FILE = "news_checkpoint.txt"

# reaction id → label
REACTION_LABELS = {
    1: "Love",
    2: "Haha",
    3: "Heart Eyes",
    4: "Wow",
    5: "Care",
    6: "Cry",
    7: "Poop",
    8: "Angry",
}

# ───────────────────────────────
# 2.  Helper: checkpoint
# ───────────────────────────────
def get_last_processed_id() -> str | None:
    """Return the last processed news_id or None."""
    with suppress(FileNotFoundError):
        return Path(CHECKPOINT_FILE).read_text().strip()
    return None


def save_last_processed_id(news_id: str) -> None:
    """Persist last processed news_id after each success."""
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(news_id)


# ───────────────────────────────
# 3.  Selenium setup
# ───────────────────────────────
chrome_opts = Options()
chrome_opts.add_argument("--headless")
chrome_opts.add_argument("--disable-gpu")
chrome_opts.add_argument("--window-size=1920,1080")
chrome_opts.add_argument("--disable-dev-shm-usage")
chrome_opts.add_argument("--no-sandbox")
# Optional: Disable images for faster loading
chrome_opts.add_argument('--blink-settings=imagesEnabled=false')

driver = webdriver.Chrome(options=chrome_opts)
wait = WebDriverWait(driver, 5)      # 10 s per element max


# ───────────────────────────────
# 4.  Main scraper
# ───────────────────────────────
def scrape_news(filename) -> None:
    last_id = get_last_processed_id()
    resume_mode = bool(last_id)

    # open NDJSON in **append** mode (create if missing)
    outfile = open(DEST_FILE, "a", encoding="utf-8")

    try:
        with open(filename, encoding="utf-8") as src:
            rows = json.load(src)

        for idx, row in enumerate(rows, 1):
            link = row.get("news_link")
            news_id = row.get("news_id")

            if not link:
                print(f"Row {idx}: missing link – skipped.")
                continue

            if resume_mode:
                if news_id == last_id:
                    # we've reached the last fully processed row → resume after it
                    resume_mode = False
                else:
                    continue  # still skipping historical rows
                # no `continue` here → we will *re-scrape* the checkpoint row itself

            print(f"[{idx}] {link}")

            try:
                driver.get(link)

                # — Author (use explicit wait) —
                try:
                    wait.until(EC.visibility_of_element_located((By.ID, "ikon_reaction_container")))
                except TimeoutException:
                    continue
                # Author info
                author_elements = driver.find_elements(By.CSS_SELECTOR, ".iauthor .name")
                if author_elements:
                    author_name = author_elements[0].text.strip()
                # — Reactions —
                reactions = []
                for box in driver.find_elements(By.CSS_SELECTOR, "#ikon_reaction_container .ikong__col"):
                    with suppress(NoSuchElementException):
                        vote_id_raw = box.find_element(By.CLASS_NAME, "vote").get_attribute("id")
                        vote_num = int(vote_id_raw.removeprefix("vote"))
                        value = box.find_element(By.CSS_SELECTOR, ".graph_inside .value").text.strip()
                        if value:
                            reactions.append(
                                {
                                    "reaction_type": REACTION_LABELS.get(vote_num, "Unknown"),
                                    "total_reactions": value,
                                }
                            )

                # — Comments —
                comments_out = []
                for com in driver.find_elements(By.CSS_SELECTOR, ".ikon-comment-container .ikoncomment"):
                    with suppress(Exception):
                        body = com.find_element(By.CLASS_NAME, "ikoncbody")
                        cvote = com.find_element(By.CLASS_NAME, "cvote").find_elements(By.TAG_NAME, "span")
                        comments_out.append(
                            {
                                "Author": body.find_element(By.CLASS_NAME, "name").text.strip(),
                                "IP Address": body.find_element(By.CLASS_NAME, "ip").text.strip(),
                                "Comment": body.find_element(By.CLASS_NAME, "comment").text.strip(),
                                "Total up vote": cvote[0].text.strip() if len(cvote) >= 1 else "N/A",
                                "Total down vote": cvote[2].text.strip() if len(cvote) >= 3 else "N/A",
                            }
                        )

                # — Assemble one record —
                record = {
                    "id": news_id,
                    "news_topic": row.get("news_topic", "N/A"),
                    "news_header": row.get("news_header", "N/A"),
                    "news_author": author_name,
                    "reactions": reactions,
                    "comments": comments_out,
                }

                # write one NDJSON line + flush
                outfile.write(json.dumps(record, ensure_ascii=False) + "\n")
                outfile.flush()
                os.fsync(outfile.fileno())

                # update checkpoint
                save_last_processed_id(news_id)

            except Exception as e:
                print(f"⚠️  Error scraping {link}: {e}")
        # finish all ids → remove checkpoint file
        with suppress(FileNotFoundError):
            os.remove(CHECKPOINT_FILE)
            print("✅ Finished – checkpoint removed.")
    except FileNotFoundError:
        print("No news file is found. Terminating script now.")
    except KeyboardInterrupt:
        print("\n🛑 Script interrupted by user. Checkpoint retained for resume.")
    finally:
        outfile.close()
        driver.quit()


# ───────────────────────────────
# 5.  Entry point
# ───────────────────────────────
if __name__ == "__main__":
    scrape_news(SOURCE_FILE)
