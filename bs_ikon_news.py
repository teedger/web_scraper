#!/usr/bin/env python3

from bs4 import BeautifulSoup
import datetime
import requests
import json
import sel_ikon_news_detailed_V2

# TODO IKON NEWS BASIC SCRAPING USING BEAUTIFUL SOUP

main_url = "https://ikon.mn/"
n_list = []
today = datetime.date.today().strftime("%Y%m%d")
file_name = f"ikon_news_{today}.json"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}

bulk_news_links = {"Politics": "l/1", "Economics": "l/2", "Society": "l/3", "Health": "l/16", "World": "l/4",
                   "Live_news": "t/58", "Technology": "l/7", "Mining": "l/20", "Bank_finance": "l/21", "Art": "l/6",
                   "Business": "l/29", "Family": "l/23", "Geopolitics": "l/52", "Education": "l/11", "Sport": "l/5",
                   "Ulaanbaatar": "l/53", "Crime": "l/12"}

def article_finder():
    news_id = 1
    for bulk_news in bulk_news_links:
        print(f"Scraping all {bulk_news} news...")
        response = requests.get(main_url + bulk_news_links[bulk_news], headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Get list of page links
        main_page = soup.find("div", class_="ikblock")
        page_control = main_page.find("div", class_="ikpagination")
        total_pages = page_control.find(class_="ikp_items").find_all(class_="ikp_item")
        # News id starts with 1
        page_links = []
        for pages in total_pages:
            page_url = pages.get("data-url")
            if page_url:
                page_link = f"https://ikon.mn/{page_url}"
                page_links.append(page_link)

        for link in page_links:
            response = requests.get(link, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            main_page = soup.find("div", class_="ikblock")
            # news_topic = main_page.find("h1").text.strip() if main_page.find("h1") else "N/A"
            news_container = main_page.find("div", class_="newslistcontainer")
            news_list = news_container.find_all("div", class_="nlitem") if news_container else []
            for news in news_list:

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

        # Save to JSON
        with open(file_name, mode="w", encoding="utf-8") as json_file:
            json.dump(n_list, json_file, ensure_ascii=False, indent=4)

        print(f"✅ Data saved to {file_name}")
        print(f"Finished all {bulk_news} news.")
    print("Finished all news topics! The program will stop now.")

if __name__ == "__main__":
    article_finder()
    sel_ikon_news_detailed_V2.scrape_news(file_name)

