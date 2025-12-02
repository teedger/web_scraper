from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import datetime
import csv

# TODO - ZANGIA.MN JOB LIST SCRAPING USING SELENIUM

main_url = "https://www.zangia.mn/job/list"

# Create empty lists for collecting data
ad_list = []
today = datetime.date.today().strftime("%Y%m%d")

# File names
file_name = f"job_list_{today}.csv"


def ad_finder():
    # --- Selenium Setup ---
    # Optional: Run in headless mode (without opening a browser window)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 5)

    try:
        # Navigate to the main page to find the last page number
        driver.get(main_url)

        # --- FIX: Restore dynamic finding of the last page number ---
        try:
            last_page_element = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "last"))
            )
            href = last_page_element.get_attribute("href")
            l_page = int(href.split("pg.")[-1].strip())
            print(f"Found {l_page} pages to scrape.")
        except (TimeoutException, AttributeError, ValueError):
            print("Could not determine the last page number. Defaulting to 100.")
            l_page = 102

        for n in range(1, 5):
            try:
                # Navigate to the specific page URL
                url = f"{main_url}?page={n}"
                driver.get(url)
                print(f"Scraping page: {n}")

                # Find the main container for job ads
                main_element = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.rounded-xl.bg-white.w-full"))
                )
                ads = main_element.find_elements(By.CSS_SELECTOR, "div.px-4.py-3.flex.items-center.gap-4")

                # Find details of elements
                for ad in ads:
                    try:
                        # Using try-except blocks for each element is more robust
                        try:
                            company_el = ad.find_element(By.CSS_SELECTOR, "a.inline-block.max-w-max.text-xs")
                            company_name = company_el.text.strip()
                            company_link = company_el.get_attribute("href")
                        except NoSuchElementException:
                            company_name = "N/A"
                            company_link = "N/A"

                        try:
                            ad_el = ad.find_element(By.CSS_SELECTOR, "a.text-sm.leading-none.tracking-normal")
                            ad_name = ad_el.text.strip()
                            ad_link = ad_el.get_attribute("href")
                        except NoSuchElementException:
                            ad_name = "N/A"
                            ad_link = "N/A"

                        try:
                            salary = ad.find_element(By.CSS_SELECTOR, "div.flex.flex-row.items-center > p").text.strip()
                        except NoSuchElementException:
                            salary = "N/A"

                        # --- THIS IS THE NEW, CORRECTED LOGIC ---
                        try:
                            location = "N/A"
                            post_date = "N/A"

                            location_date_div = ad.find_element(By.CSS_SELECTOR, "div.flex.flex-col.items-end.w-24")
                            p_tags = location_date_div.find_elements(By.CSS_SELECTOR, "p")

                            for p_tag in p_tags:
                                text = p_tag.text.strip()
                                if not text:
                                    continue

                                # Heuristic: If it contains numbers or Mongolian date words, it's a date.
                                if any(keyword in text for keyword in ['2025', '2024', '2023']) or any(
                                        char.isdigit() for char in text):
                                    # Pass the raw text to our new parsing function
                                    post_date = text
                                else:
                                    # Otherwise, assume it's the location
                                    location = text

                        except NoSuchElementException:
                            # This block runs if the parent div itself is not found
                            location = "N/A"
                            post_date = "N/A"

                        ad_dict = {
                            "company_name": company_name,
                            "company_link": company_link,  # Selenium provides the full URL
                            "ad_name": ad_name,
                            "ad_link": ad_link,  # Selenium provides the full URL
                            "salary": salary,
                            "location": location,
                            "post_date": post_date,
                        }
                        ad_list.append(ad_dict)

                    except Exception as e:
                        print(f"Error processing an individual ad listing: {e}")

            except Exception as e:
                print(f"An error occurred on page {n}: {url} - {e}")

    finally:
        # Ensure the browser is closed even if an error occurs
        driver.quit()

    if ad_list:
        with open(file_name, mode="w", newline='', encoding='utf-8') as file:
            fieldnames = ad_list[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(ad_list)
        print(f"Data successfully saved to {file_name}")
    else:
        print("There are no ad list available. Please try again.")


if __name__ == "__main__":
    ad_finder()
