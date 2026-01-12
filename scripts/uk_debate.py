from bs4 import BeautifulSoup
import cloudscraper
from selenium.common import NoSuchElementException
import time
import re
import csv
import os

# Create a cloudscraper instance
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'darwin',  # MacOS
        'mobile': False,
    }
)

def debate_link_scraper():
    start_date = "1971-01-01"
    end_date = "1974-12-31"
    search_terms = ["Northern+Ireland", "Northern+Irish", "Belfast"]
    for search_term in search_terms:
        print("Starting debate link scrape for search term: ", search_term)
        url = f"https://hansard.parliament.uk/search/Debates?startDate={start_date}&endDate={end_date}&searchTerm={search_term}&partial=True&sortOrder=1"

        response = scraper.get(url)
        time.sleep(1)

        soup = BeautifulSoup(response.content, "html.parser")

        file_name = "../output/debate_links.csv"

        debates_list = []
        try:
            # Find the last page of the result
            page_text = soup.find("div", class_="result-text").text.strip()
            result = re.search(r"page (\d+) of (\d+)", page_text)
            last_page = result.group(2)
            print("Last page found: ", last_page)

            if last_page:
                for n in range(1, int(last_page) + 1):
                    try:
                        print("Processing page number ", n)
                        response = scraper.get(url + f"&page={n}")
                        time.sleep(1)
                        soup = BeautifulSoup(response.content, "html.parser")
                        debate_cards = soup.find("div", class_="card-list")
                        links = debate_cards.find_all("a", class_="card card-calendar")
                        for link in links:
                            href = "https://hansard.parliament.uk" + link["href"]
                            title = link.find("div", class_="primary-info").text.strip()
                            date = link.find("div", class_="secondary-info").text.strip()
                            chamber = link.find("div", class_="indicators-left").find("div", class_="indicator").text.strip()
                            debates_list.append({"title": title, "date": date, "chamber": chamber, "href": href})

                    except Exception as e:
                        print(f"Error processing url: {url}&page={n} - {e}")

        except AttributeError:
            print(f"Could not find any debates for this search term: {search_term}")

        if debates_list:
            if os.path.exists(file_name):
                with open(file_name, mode="a", newline='', encoding='utf-8') as file:
                    fieldnames = debates_list[0].keys()
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writerows(debates_list)
            else:
                with open(file_name, mode="w", newline='', encoding='utf-8') as file:
                    fieldnames = debates_list[0].keys()
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(debates_list)

def debate_scraper(filename):
    destination_file_name = "../output/debates.csv"

    # Field names for csv
    fieldnames = ["text", "speaker", "political_party", "date"]

    with open(filename, mode="r", encoding="utf-8") as source_file:
        csv_reader = csv.DictReader(source_file)
        with open(destination_file_name, mode="a", newline="", encoding="utf-8") as dest_file:
            writer = csv.DictWriter(dest_file, fieldnames=fieldnames)

            # Write header only if the destination file is empty
            if os.stat(destination_file_name).st_size == 0:
                writer.writeheader()

            for idx, row in enumerate(csv_reader, start=1):
                debate_link = row.get("href")
                date = row.get("date")
                chamber = row.get("chamber")

                if not debate_link:
                    print(f"Missing debate link in row {idx}. Skipping...")
                    continue

                print(f"Processing {idx}: {debate_link}")
                try:
                    response = scraper.get(debate_link)
                    soup = BeautifulSoup(response.text, "html.parser")
                    debates = soup.find_all("div", class_="debate-item debate-item-contributiondebateitem")
                    # print(debates)
                    for debate in debates:
                        debate_header = debate.find("div", class_="header")
                        debate_item = debate_header.find("div", class_="item")
                        debate_detail = debate_item.find("div", class_="attributed-to-details")
                        speaker_name = debate_detail.find("div", class_="primary-text").text.strip()
                        debate_content = debate.find("div", class_="content")
                        debate_text = debate_content.find("p").text.strip()
                        # Write data immediately
                        writer.writerow({"text": debate_text, "speaker": speaker_name, "political_party": chamber, "date": date})

                except Exception as e:
                    print(f"Error processing url: {debate_link} - {e}")

if __name__ == "__main__":
    # print("Starting debate link scraper...")
    # debate_link_scraper()
    # time.sleep(2)
    if os.path.exists("../output/debate_links.csv"):
        print("Starting debate scraper...")
        debate_scraper("../output/debate_links.csv")
