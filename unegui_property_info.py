from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import datetime
import csv

# TODO - UNEGUI.MN PROPERTY INFORMATION SCRAPING

# Deploy Selenium
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# Create empty list and dict
house_list = []
today = datetime.date.today().strftime("%Y%m%d")

# File names
source_file_name = "property_list_20241109.csv"
destination_file_name = f"property_info_{today}.csv"


fieldnames = ["id", "floor", "balcony", "date_of_commission", "garage", "window_material", "total_floor", "door_material",
              "sq_m", "which_floor", "payment_term", "window_count", "elevator"]

def property_info():
    # Open the CSV file
    with open(source_file_name, mode='r', encoding='utf-8') as target_file:
        csv_reader = csv.DictReader(target_file)
        for row in csv_reader:
            link_text = row["ad_link"]
            building_info = {}
            try:
                driver.get(link_text)
                ad_id = driver.find_element(By.CSS_SELECTOR, ".number-announcement span").text
                building_info["id"] = ad_id
                info_list = driver.find_elements(By.CSS_SELECTOR, ".chars-column li")
                for info in info_list:
                    try:
                        key_element = info.find_element(By.CLASS_NAME, 'key-chars')
                        value_element = info.find_element(By.CLASS_NAME, 'value-chars')
                        # Check if key_element text is "Шал"
                        if key_element.text == "Шал:":
                            building_info["floor"] = value_element.text
                        elif key_element.text == "Тагт:":
                            building_info["balcony"] = value_element.text
                        elif key_element.text == "Ашиглалтанд орсон он:":
                            building_info['date_of_commission'] = value_element.text
                        elif key_element.text == "Гараж:":
                            building_info['garage'] = value_element.text
                        elif key_element.text == "Цонх:":
                            building_info['window_material'] = value_element.text
                        elif key_element.text == "Барилгын давхар:":
                            building_info["total_floor"] = value_element.text
                        elif key_element.text == "Хаалга:":
                            building_info["door_material"] = value_element.text
                        elif key_element.text == "Талбай:":
                            building_info["sq_m"] = value_element.text
                        elif key_element.text == "Хэдэн давхарт:":
                            building_info["which_floor"] = value_element.text
                        elif key_element.text == "Төлбөрийн нөхцөл:":
                            building_info["payment_term"] = value_element.text
                        elif key_element.text == "Цонхны тоо:":
                            building_info["window_count"] = value_element.text
                        elif key_element.text == "Цахилгаан шаттай эсэх:":
                            building_info["elevator"] = value_element.text
                    except NoSuchElementException:
                        print("Element not found. Continuing with the rest of the code.")
                house_list.append(building_info)
            except Exception as e:
                print(f"Could not click on link: {link_text} - {e}")
            with open(destination_file_name, mode="w", newline='', encoding='utf-8') as dest_file:
                writer = csv.DictWriter(dest_file, fieldnames=fieldnames)
                if fieldnames:
                    writer.writeheader()
                writer.writerows(house_list)
    driver.quit()

property_info()
