from bs4 import BeautifulSoup
import datetime
import csv
import requests

# TODO - ZANGIA.MN JOB LIST SCRAPING USING BEAUTIFUL SOUP

main_url = f"https://www.zangia.mn/job/list"

# Create empty lists for collecting data
ad_list = []
today = datetime.date.today().strftime("%Y%m%d")

# File names
file_name = f"job_list_{today}.csv"

def ad_finder():
    # Deploy Beautiful Soup
    response = requests.get(main_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the last page number
    last_page_link = soup.find(class_="page-link")
    if last_page_link:
        last_page = last_page_link.find(class_="last")
        if last_page:
            href = last_page.get("href")
            l_page = int(href.split("pg.")[-1].strip()) if href else 100
        else:
            l_page = 100
    else:
        l_page = 100
    print(l_page)
    for n in range(1, l_page + 1):
        try:
            # Deploy Beautiful Soup
            url = f"{main_url}?page={n}"
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the ad elements inside the main element
            main_element = soup.find("div", class_="rounded-xl bg-white w-full")
            if main_element:
                ads = main_element.find_all('div', class_="px-4 py-3 flex items-center gap-4")
            else:
                print("Main element with class 'rounded-xl bg-white w-full' not found.")
                ads = []

            # Find details of elements
            for ad in ads:
                try:
                    company = ad.find("a", class_="inline-block max-w-max text-xs")
                    company_name = company.text.strip() if company and company.text else "N/A"
                    company_link = company.get("href") if company and company.get("href") else "N/A"
                    ad_name = (ad.find("a", class_="text-sm leading-none tracking-normal").
                               text.strip()) if (ad.find("a", class_="text-sm leading-none tracking-normal") and
                                                 ad.find("a", class_="text-sm leading-none tracking-normal").text) else "N/A"
                    ad_link = ad.find("a", class_="text-sm leading-none tracking-normal").get("href") if (
                            ad.find("a", class_="text-sm leading-none tracking-normal") and
                            ad.find("a", class_="text-sm leading-none tracking-normal").get("href")) else "N/A"
                    salary_div = ad.find("div", class_="flex flex-row items-center")
                    salary = salary_div.find("p").text if salary_div and salary_div.find("p") else "N/A"
                    location_date_div = ad.find("div", class_="group p-2 cursor-pointer")
                    location_el = location_date_div.find("p", class_="text-[10px] text-[#28292A]/[72] text-right") if location_date_div else None
                    location = location_el.text.strip() if location_el and location_date_div else "N/A"
                    date_el = location_date_div.find("p", class_="text-[10px] text-[#28292A]/[72]") if location_date_div else None
                    post_date = date_el.text.strip() if date_el and location_date_div else "N/A"
                    ad_dict = {
                        "company_name": company_name,
                        "company_link": f"https://www.zangia.mn/{company_link}",
                        "ad_name": ad_name,
                        "ad_link": f"https://www.zangia.mn/{ad_link}",
                        "salary": salary,
                        "location": location,
                        "post_date": post_date,
                    }
                    ad_list.append(ad_dict)
                except AttributeError:
                    print("Element not found. Continuing with the rest of the code.")
        except Exception as e:
            print(f"An error occurred: {main_url}?page={n} - {e}")
    if ad_list:
        with open(file_name, mode="w", newline='', encoding='utf-8') as file:
            fieldnames = ad_list[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(ad_list)
    else:
        print("There are no ad list available. Please try again.")

if __name__ == "__main__":
    ad_finder()
