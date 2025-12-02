from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import csv
import datetime

# TODO - ZANGIA.MN COMPANY INFO SCRAPING

main_url = f"https://www.zangia.mn/company"

# Create empty lists for collecting data
company_list = []
today = datetime.date.today().strftime("%Y%m%d")

# File names
file_name = f"company_list_{today}.csv"

def com_finder():
    # Deploy Selenium
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    # Get the last page number from the first page
    driver.get(main_url)
    last_page = driver.find_element(By.CSS_SELECTOR, ".page-link .last").get_attribute("href")
    l_page = int(last_page.split("pg.")[-1].strip())
    print(l_page)
    for n in range(1, l_page + 1):
        try:
            # Deploy selenium
            url = f"{main_url}/pg.{n}"
            driver.get(url)

            # Find the main element
            companies = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'company-')]")
            for company in companies:
                try:
                    company_name = company.find_element(By.CSS_SELECTOR, "a b").text
                    company_link = company.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    company_logo = company.find_element(By.CSS_SELECTOR, "a img").get_attribute("src")
                    description = company.find_element(By.CSS_SELECTOR, "span").text
                    com_dict = {
                        "company_name": company_name,
                        "company_link": company_link,
                        "company_logo": company_logo,
                        "description": description
                    }
                    company_list.append(com_dict)
                except NoSuchElementException:
                    print("Element not found. Continuing with the rest of the code.")
            with open(file_name, mode="w", newline='', encoding='utf-8') as file:
                fieldnames = company_list[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(company_list)
        except Exception as e:
            print(f"Could not click on link: {main_url}/pg.{n} - {e}")
    driver.quit()

com_finder()
