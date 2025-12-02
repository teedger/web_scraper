from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import datetime
import csv

# TODO - UNEGUI.MN CAR LIST SCRAPING

main_url = "https://www.unegui.mn/avto-mashin/-avtomashin-zarna/"

# Create empty lists for collecting data
ad_list = []
today = datetime.date.today().strftime("%Y%m%d")

# File names
file_name = f"car_list_{today}.csv"

def ad_finder():
    # Deploy Selenium
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    # Get the last page number from the first page
    driver.get(main_url)
    page_count = driver.find_elements(By.CSS_SELECTOR, ".number-list li")
    last_page = int(page_count[len(page_count) - 1].find_element(By.TAG_NAME, "a").text)
    for n in range(1, last_page):
        try:
            # Deploy selenium
            url = f"{main_url}?page={n}"
            driver.get(url)

            # Find the main list element
            main_element = driver.find_element(By.CSS_SELECTOR, "#listing .wrap")
            ads = main_element.find_elements(By.XPATH, "//*[string-length(@id)=7 and number(@id)]")
            for ad in ads:
                try:
                    ad_id = ad.get_attribute("id")
                    ad_title = ad.find_element(By.CSS_SELECTOR, ".advert__content-title").text
                    price = ad.find_element(By.CSS_SELECTOR, ".advert__content-header a span").text
                    currency = ad.find_element(By.CSS_SELECTOR, ".advert__content-header a span b").text
                    ad_link = ad.find_element(By.CSS_SELECTOR, ".advert__content-header a")
                    ad_link_text = ad.find_element(By.CSS_SELECTOR, ".advert__content-header a").get_attribute("href")
                    ad_date = ad.find_element(By.CSS_SELECTOR, ".advert__content-date").text
                    location = ad.find_element(By.CSS_SELECTOR, ".advert__content-place").text
                    ad_dict = {
                        "id": ad_id,
                        "ad_title": ad_title,
                        "price": price,
                        "currency": currency,
                        "ad_link": ad_link_text,
                        "ad_date": ad_date,
                        "location": location,
                    }
                    ad_list.append(ad_dict)
                except NoSuchElementException:
                    print("Element not found. Continuing with the rest of the code.")
            with open(file_name, mode="w", newline='', encoding='utf-8') as file:
                fieldnames = ad_list[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(ad_list)
        except Exception as e:
            print(f"Could not click on link: {main_url}?page={n} - {e}")
    driver.quit()

ad_finder()




