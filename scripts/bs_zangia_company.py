from bs4 import BeautifulSoup
import datetime
import csv
import requests

# TODO - ZANGIA.MN COMPANY LIST SCRAPING USING BEAUTIFUL SOUP

main_url = "https://www.zangia.mn/"

# Create empty lists for collecting data
company_list = []
today = datetime.date.today().strftime("%Y%m%d")

# File names
file_name = f"../output/company_list_{today}.csv"

def com_finder():
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
            url = f"{main_url}company/pg.{n}"
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the ad elements inside the main element
            main_element = soup.find("div", class_="companies")
            if main_element:
                companies = main_element.find_all('div', id=lambda x: x and x.startswith('company-'))
            else:
                print("List of companies not found.")
                companies = []

            # Find details of elements
            for company in companies:
                try:
                    company_name = company.find("a").find("b").text.strip() if company.find("a") else "N/A"
                    company_link = company.find("a").get("href") if company.find("a") else "N/A"
                    company_logo = company.find("a").find("img").get("src") if company.find("a").find("img") else "N/A"
                    description = company.find("span").text.strip() if company.find("span") else "N/A"
                    com_dict = {
                        "company_name": company_name,
                        "company_link": f"{main_url}{company_link}",
                        "company_logo": f"{main_url}{company_logo}",
                        "description": description
                    }
                    company_list.append(com_dict)
                except AttributeError:
                    print("Element not found. Continuing with the rest of the code.")
        except Exception as e:
            print(f"An error occurred: {main_url}/pg.{n} - {e}")
    if company_list:
        with open(file_name, mode="w", newline='', encoding='utf-8') as file:
            fieldnames = company_list[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(company_list)
    else:
        print("There are no company list available. Please try again.")


if __name__ == "__main__":
    com_finder()
