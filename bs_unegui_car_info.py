import os
from bs4 import BeautifulSoup
import datetime
import csv
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


# TODO - UNEGUI.MN CAR INFORMATION SCRAPING USING BEAUTIFUL SOUP

# Create empty list and dict
car_list = []
today = datetime.date.today().strftime("%Y%m%d")

# File names
source_file_name = f"car_list_{today}.csv"
destination_file_name = f"car_info_{today}.csv"
checkpoint_file = "car_checkpoint.txt"  # File to track the last processed ad_id

# Field names for csv
fieldnames = ["id", "engine_cap", "transmission", "steering", "type", "color", "manufacture_year", "import_year",
              "engine_type", "inter_color", "leasing", "drive", "mileage", "condition", "doors"]

# Retry logic for HTTP requests
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount("http://", HTTPAdapter(max_retries=retries))
session.mount("https://", HTTPAdapter(max_retries=retries))

def get_last_processed_id():
    """Read the last processed ad_id from the checkpoint file."""
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, "r") as file:
            return file.read().strip()
    return None


def save_last_processed_id(ad_id):
    """Save the last processed ad_id to the checkpoint file."""
    with open(checkpoint_file, "w") as file:
        file.write(ad_id)


def car_info(filename):
    # Get the last processed ad_id
    last_processed_id = get_last_processed_id()
    resume = False if not last_processed_id else True

    with open(filename, mode="r", encoding="utf-8") as source_file:
        csv_reader = csv.DictReader(source_file)
        with open(destination_file_name, mode="a", newline="", encoding="utf-8") as dest_file:
            writer = csv.DictWriter(dest_file, fieldnames=fieldnames)

            # Write header only if the destination file is empty
            if os.stat(destination_file_name).st_size == 0:
                writer.writeheader()
            final_idx = 0     # To get the length of the csv file later on.
            for idx, row in enumerate(csv_reader, start=1):
                link_text = row.get("ad_link")
                ad_id = row.get("id")  # Assuming "id" is a column in the source CSV

                if not link_text:
                    print(f"Missing ad_link in row {idx}. Skipping...")
                    continue

                # Skip already processed rows
                if resume and ad_id == last_processed_id:
                    print(f"Resuming from row {idx + 1}...")
                    resume = False  # Resume processing from the next row
                    continue
                elif resume:
                    continue

                print(f"Processing {idx}: {link_text}")
                try:
                    response = session.get(link_text)
                    response.raise_for_status()
                    response.encoding = response.apparent_encoding
                    soup = BeautifulSoup(response.text, "html.parser")

                    # Extract ad ID
                    number_announcement = soup.find(class_="number-announcement")
                    ad_id = number_announcement.find("span").text.strip() if number_announcement else None
                    if not ad_id:
                        print(f"Ad ID not found for {link_text}. Skipping...")
                        continue

                    # Initialize car info
                    car_dict = {
                        "id": ad_id,
                        "engine_cap": None, "transmission": None, "steering": None,
                        "type": None, "color": None, "manufacture_year": None,
                        "import_year": None, "engine_type": None, "inter_color": None,
                        "leasing": None, "drive": None, "mileage": None,
                        "condition": None, "doors": None
                    }

                    # Extract building details
                    info_list = soup.find(class_="chars-column")
                    if info_list:
                        li = info_list.find_all("li")
                        for info in li:
                            key_element = info.find(class_="key-chars")
                            value_element = info.find(class_="value-chars")
                            if key_element and value_element:
                                key_text = key_element.text.strip()
                                value_text = value_element.text.strip()
                                if key_text == "Мотор багтаамж:":
                                    car_dict["engine_cap"] = value_text
                                elif key_text == "Хурдны хайрцаг:":
                                    car_dict["transmission"] = value_text
                                elif key_text == "Хүрд:":
                                    car_dict['steering'] = value_text
                                elif key_text == "Төрөл:":
                                    car_dict['type'] = value_text
                                elif key_text == "Өнгө:":
                                    car_dict['color'] = value_text
                                elif key_text == "Үйлдвэрлэсэн он:":
                                    car_dict["manufacture_year"] = value_text
                                elif key_text == "Орж ирсэн он:":
                                    car_dict["import_year"] = value_text
                                elif key_text == "Хөдөлгүүр:":
                                    car_dict["engine_type"] = value_text
                                elif key_text == "Дотор өнгө:":
                                    car_dict["inter_color"] = value_text
                                elif key_text == "Лизинг:":
                                    car_dict["leasing"] = value_text
                                elif key_text == "Хөтлөгч:":
                                    car_dict["drive"] = value_text
                                elif key_text == "Явсан:":
                                    car_dict["mileage"] = value_text
                                elif key_text == "Нөхцөл:":
                                    car_dict["condition"] = value_text
                                elif key_text == "Хаалга:":
                                    car_dict["doors"] = value_text

                    # Write data immediately
                    writer.writerow(car_dict)

                    # Save progress
                    save_last_processed_id(ad_id)

                    final_idx += 1

                except requests.exceptions.RequestException as e:
                    print(f"HTTP error while processing {link_text}: {e}")
                except Exception as e:
                    print(f"Error processing {link_text}: {e}")
            if dest_file:
                print("=" * 60)
                print("\nFinished the script. Total ads scraped: {}\n".format(final_idx))

    if os.path.exists(checkpoint_file):
        os.remove(checkpoint_file)
        print("Deleted checkpoint file")

if __name__ == "__main__":
    car_info(source_file_name)
