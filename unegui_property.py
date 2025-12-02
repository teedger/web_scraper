from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import csv
from tqdm import tqdm

# TODO - UNEGUI.MN PROPERTY LIST SCRAPING

main_url = "https://www.unegui.mn/l-hdlh/l-hdlh-zarna/"

# Create empty lists for collecting data
ad_list = []
today = datetime.date.today().strftime("%Y%m%d")

# File names
file_name = f"property_list_{today}.csv"

def ad_finder():
    # Deploy Selenium with optimizations to bypass bot detection
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Add user agent to avoid bot detection
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)

    # Hide webdriver property to avoid detection
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        '''
    })

    # Get the last page number from the first page
    driver.get(main_url)

    try:
        page_count = driver.find_elements(By.CSS_SELECTOR, ".number-list li")
        last_page = int(page_count[len(page_count) - 1].find_element(By.TAG_NAME, "a").text)
        print("Last page found: ", last_page)
    except (IndexError, NoSuchElementException, ValueError) as e:
        print(f"Could not find last page number: {e}. Defaulting to page 1.")
        last_page = 2  # Will scrape only page 1

    # Scrape each page with progress bar
    for n in tqdm(range(1, last_page), desc="Scraping pages", unit="page"):
        try:
            url = f"{main_url}?page={n}"
            driver.get(url)

            # Wait for the main list element to load
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#listing")))

            # Find all ads directly
            ads = driver.find_elements(By.XPATH, "//*[@id='listing']//*[string-length(@id)=7 and number(@id)]")
            for ad in ads:
                try:
                    ad_id = ad.get_attribute("id")
                    ad_title = ad.find_element(By.CSS_SELECTOR, ".advert__content-title").text
                    price = ad.find_element(By.CSS_SELECTOR, ".advert__content-header a span").text
                    currency = ad.find_element(By.CSS_SELECTOR, ".advert__content-header a span b").text
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

if __name__ == "__main__":
    ad_finder()


