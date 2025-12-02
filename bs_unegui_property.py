#!/usr/bin/env python3
from bs4 import BeautifulSoup
import datetime
import csv
import requests
import bs_unegui_property_info
try:
    from tqdm.auto import tqdm
except ModuleNotFoundError:  # no tqdm? use noop wrapper
    def tqdm(iterable=None, **kw):  # type: ignore
        return iterable if iterable is not None else lambda x: x

# TODO - UNEGUI.MN PROPERTY LIST SCRAPING USING BEAUTIFUL SOUP

main_url = "https://www.unegui.mn/l-hdlh/l-hdlh-zarna/"

# Create empty lists for collecting data
ad_list = []
today = datetime.date.today().strftime("%Y%m%d")

# File names
file_name = f"property_list_{today}.csv"

def ad_finder():
    # Deploy Beautiful Soup
    try:
        response = requests.get(main_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the last page number
        page_list_ul = soup.find('ul', class_='number-list')
        li_elements = page_list_ul.find_all('li') if page_list_ul else []
        if li_elements:
            last_page_text = li_elements[-1].find('a').text if li_elements[-1].find('a') else "1"
            last_page = int(last_page_text)
        else:
            last_page = 1
        print(f"Last page found: {last_page}")

        for n in range(1, 2):
            try:
                # Deploy Beautiful Soup
                url = f"{main_url}?page={n}"
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find the main list element
                main_element = soup.find(id="listing").find(class_="wrap")
                if main_element:
                    elements = main_element.find_all(True)  # Find all tags inside the wrap element
                    matching_elements = []

                    # Check if element has id with 7 digits
                    for element in elements:
                        element_id = element.get('id')
                        if element_id and len(element_id) == 7 and element_id.isdigit():
                            matching_elements.append(element)

                    # Find details of elements
                    for element in matching_elements:
                        try:
                            ad_id = element.get('id')
                            ad_title = element.find(class_="advert__content-title").text.strip() if (
                                element.find(class_="advert__content-title")) else "N/A"
                            price = element.find(class_="advert__content-header").find("a").find("span").text.strip() if (
                                element.find(class_="advert__content-header").find("a")) else "N/A"
                            currency = element.find(class_="advert__content-header").find("a").find("span").find("b").text.strip() if (
                                element.find(class_="advert__content-header").find("a").find("span").find("b")) else "N/A"
                            ad_link = element.find(class_="advert__content-header").find("a").get("href").strip() if (
                                element.find(class_="advert__content-header").find("a")) else "N/A"
                            ad_date = element.find(class_="advert__content-date").text.strip() if (
                                element.find(class_="advert__content-date")) else "N/A"
                            location = element.find(class_="advert__content-place").text.strip() if (
                                element.find(class_="advert__content-place")) else "N/A"
                            ad_dict = {
                                "id": ad_id,
                                "ad_title": ad_title,
                                "price": price,
                                "currency": currency,
                                "ad_link": f"https://unegui.mn{ad_link}",
                                "ad_date": ad_date,
                                "location": location,
                            }
                            ad_list.append(ad_dict)
                        except AttributeError:
                            print("Element not found. Continuing with the rest of the code.")
                    with open(file_name, mode="w", newline='', encoding='utf-8') as file:
                        fieldnames = ad_list[0].keys()
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(ad_list)
            except Exception as e:
                print(f"Error processing url: {main_url}?page={n} - {e}")
    except Exception as e:
        print(f"Error fetching main URL: {e}")

if __name__ == "__main__":
    ad_finder()
    print("=" * 60)
    print("\nStarting the property detailed info script now. Total ads scraped: {}\n".format(len(ad_list)))
    bs_unegui_property_info.property_info(file_name)
