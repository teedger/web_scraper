from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import datetime
import csv

# TODO - UNEGUI.MN CAR INFORMATION SCRAPING

# Deploy Selenium
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# Create empty list and dict
car_list = []
today = datetime.date.today().strftime("%Y%m%d")

# File names
source_file_name = "car_list_20241111.csv"
destination_file_name = f"car_info_{today}.csv"


fieldnames = ["id", "engine_cap", "transmission", "steering", "type", "color", "manufacture_year", "import_year",
              "engine_type", "inter_color", "leasing", "drive", "mileage", "condition", "doors"]

def car_info():
    # Open the CSV file
    with open(source_file_name, mode='r', encoding='utf-8') as target_file:
        csv_reader = csv.DictReader(target_file)
        for row in csv_reader:
            link_text = row["ad_link"]
            car_dict = {}
            try:
                driver.get(link_text)
                ad_id = driver.find_element(By.CSS_SELECTOR, ".number-announcement span").text
                car_dict["id"] = ad_id
                info_list = driver.find_elements(By.CSS_SELECTOR, ".chars-column li")
                for info in info_list:
                    try:
                        key_element = info.find_element(By.CLASS_NAME, 'key-chars')
                        value_element = info.find_element(By.CLASS_NAME, 'value-chars')
                        # Check if key_element text is "Шал"
                        if key_element.text == "Мотор багтаамж:":
                            car_dict["engine_cap"] = value_element.text
                        elif key_element.text == "Хурдны хайрцаг:":
                            car_dict["transmission"] = value_element.text
                        elif key_element.text == "Хүрд:":
                            car_dict['steering'] = value_element.text
                        elif key_element.text == "Төрөл:":
                            car_dict['type'] = value_element.text
                        elif key_element.text == "Өнгө:":
                            car_dict['color'] = value_element.text
                        elif key_element.text == "Үйлдвэрлэсэн он:":
                            car_dict["manufacture_year"] = value_element.text
                        elif key_element.text == "Орж ирсэн он:":
                            car_dict["import_year"] = value_element.text
                        elif key_element.text == "Хөдөлгүүр:":
                            car_dict["engine_type"] = value_element.text
                        elif key_element.text == "Дотор өнгө:":
                            car_dict["inter_color"] = value_element.text
                        elif key_element.text == "Лизинг:":
                            car_dict["leasing"] = value_element.text
                        elif key_element.text == "Хөтлөгч:":
                            car_dict["drive"] = value_element.text
                        elif key_element.text == "Явсан:":
                            car_dict["mileage"] = value_element.text
                        elif key_element.text == "Нөхцөл:":
                            car_dict["condition"] = value_element.text
                        elif key_element.text == "Хаалга:":
                            car_dict["doors"] = value_element.text
                    except NoSuchElementException:
                        print("Element not found. Continuing with the rest of the code.")
                car_list.append(car_dict)
            except Exception as e:
                print(f"Could not click on link: {link_text} - {e}")
            with open(destination_file_name, mode="w", newline='', encoding='utf-8') as dest_file:
                writer = csv.DictWriter(dest_file, fieldnames=fieldnames)
                if fieldnames:
                    writer.writeheader()
                writer.writerows(car_list)
    driver.quit()

car_info()
