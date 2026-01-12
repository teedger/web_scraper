from bs4 import BeautifulSoup
import datetime
import csv
import cloudscraper
import os

# UNEGUI.MN Job List Scraper

# Create a cloudscraper instance
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'darwin',  # MacOS
        'mobile': False
    }
)
main_url = "https://www.unegui.mn/azhild-avna/"

# Data Collection
ad_list = []
today = datetime.date.today().strftime("%Y%m%d")
file_name = f"../output/unegui_job_list_{today}.csv"

def ad_finder():
    response = scraper.get(main_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find last page number
    page_list_ul = soup.find("ul", class_="number-list")
    li_elements = page_list_ul.find_all("li") if page_list_ul else []
    last_page = int(li_elements[-1].find("a").text) if li_elements and li_elements[-1].find("a") else 50

    print(f"Last page found: {last_page}")

    for n in range(1, last_page + 1):
        try:
            url = f"{main_url}?page={n}"
            response = scraper.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            # Find job listings
            main_element = soup.find(id="listing").find(class_="wrap")
            if main_element:
                elements = main_element.find_all(class_="announcement-container")

                for element in elements:
                    try:
                        # Extract data-id from "announcement-block__favorites"
                        div_element = element.find("div", class_=lambda x: x and x.startswith("announcement-block__favorites"))
                        element_id = div_element["data-id"] if div_element and div_element.has_attr("data-id") else "N/A"

                        # Extract job title
                        ad_title_element = element.find("a", class_="announcement-block__title")
                        ad_title = ad_title_element.text.strip() if ad_title_element else "N/A"

                        # Extract job description
                        description_element = element.find("div", class_="announcement-block__description")
                        description = description_element.text.strip() if description_element else "N/A"

                        # Extract salary
                        salary_element = element.find(class_="announcement-block__price")
                        salary = salary_element.text.strip() if salary_element else "N/A"

                        # Extract job link
                        ad_link_element = element.find("a", class_="announcement-block__title")
                        ad_link = f"https://unegui.mn{ad_link_element['href'].strip()}" if ad_link_element and ad_link_element.has_attr("href") else "N/A"

                        # Extract Date & Location safely
                        date_location = element.find("div", class_="announcement-block__date")
                        date_text = date_location.text.strip() if date_location else "N/A"
                        date_parts = date_text.split(",") if date_text else []

                        # Extract Employer
                        employer_element = element.find("div", class_="announcement-block__date").find("span")
                        employer = employer_element.text.strip() if employer_element else "N/A"

                        # Extract date and location
                        ad_date = date_parts[1].strip() if len(date_parts) > 1 else "N/A"
                        city_district = date_parts[2].strip() if len(date_parts) > 2 else "N/A"
                        district_khoroo = ' '.join(date_parts[3:5]) if len(date_parts) > 3 else "N/A"

                        # Get industry and job_type from span elements
                        span_elements = element.find("div", class_="announcement-block__breadcrumbs").find_all("span") if element.find("div", class_="announcement-block__breadcrumbs") else []
                        industry = span_elements[0].text.strip() if len(span_elements) >= 1 else "N/A"
                        job_type = span_elements[1].text.strip() if len(span_elements) >= 2 else "N/A"

                        # Extract Premium Status
                        premium_element = element.find("div", class_=lambda x: x and x.startswith("announcement-block__job"))
                        premium_span = premium_element.find("span", class_=lambda x: x and x.startswith("announcement-block__job")) if premium_element else None
                        premium = premium_span.text.strip() if premium_span else "N/A"

                        # Store extracted data
                        job_dict = {
                            "id": element_id,
                            "ad_title": ad_title,
                            "description": description,
                            "salary": salary,
                            "employer": employer,
                            "ad_link": ad_link,
                            "ad_date": ad_date,
                            "city_district": city_district,
                            "district_khoroo": district_khoroo,
                            "industry": industry,
                            "job_type": job_type,
                            "premium": premium
                        }
                        ad_list.append(job_dict)

                    except AttributeError:
                        print("Skipping entry: Unexpected structure.")

            print(f"Scraped page {n}")

        except Exception as e:
            print(f"Error on page {n}: {e}")

    # Save to CSV
    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=ad_list[0].keys())
        writer.writeheader()
        writer.writerows(ad_list)
    print(f"Data saved to {file_name}")

if __name__ == "__main__":
    ad_finder()
