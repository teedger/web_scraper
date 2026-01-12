import os
from bs4 import BeautifulSoup
import datetime
import csv
import cloudscraper

# Create a cloudscraper instance
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'darwin',  # MacOS
        'mobile': False
    }
)

# Initialize variables
house_list = []
today = datetime.date.today().strftime("%Y%m%d")

# File names
source_file_name = f"../output/property_list_{today}.csv"
destination_file_name = f"../output/property_info_{today}.csv"
checkpoint_file = "property_checkpoint.txt"  # File to track the last processed ad_id

# Field names for csv
fieldnames = ["id", "floor", "balcony", "date_of_commission", "garage", "window_material", "total_floor",
              "door_material",
              "sq_m", "which_floor", "payment_term", "window_count", "elevator"]

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


def property_info(filename):
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

            final_idx = 0  # To get the length of the csv file later on.

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
                    response = scraper.get(link_text)
                    soup = BeautifulSoup(response.text, "html.parser")

                    # Extract ad ID
                    number_announcement = soup.find(class_="number-announcement")
                    ad_id = number_announcement.find("span").text.strip() if number_announcement else None
                    if not ad_id:
                        print(f"Ad ID not found for {link_text}. Skipping...")
                        continue

                    # Initialize building info
                    building_info = {
                        "id": ad_id,
                        "floor": None, "balcony": None, "date_of_commission": None,
                        "garage": None, "window_material": None, "total_floor": None,
                        "door_material": None, "sq_m": None, "which_floor": None,
                        "payment_term": None, "window_count": None, "elevator": None
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
                                if key_text == "Шал:":
                                    building_info["floor"] = value_text
                                elif key_text == "Тагт:":
                                    building_info["balcony"] = value_text
                                elif key_text == "Ашиглалтанд орсон он:":
                                    building_info["date_of_commission"] = value_text
                                elif key_text == "Гараж:":
                                    building_info["garage"] = value_text
                                elif key_text == "Цонх:":
                                    building_info["window_material"] = value_text
                                elif key_text == "Барилгын давхар:":
                                    building_info["total_floor"] = value_text
                                elif key_text == "Хаалга:":
                                    building_info["door_material"] = value_text
                                elif key_text == "Талбай:":
                                    building_info["sq_m"] = value_text
                                elif key_text == "Хэдэн давхарт:":
                                    building_info["which_floor"] = value_text
                                elif key_text == "Төлбөрийн нөхцөл:":
                                    building_info["payment_term"] = value_text
                                elif key_text == "Цонхны тоо:":
                                    building_info["window_count"] = value_text
                                elif key_text == "Цахилгаан шаттай эсэх:":
                                    building_info["elevator"] = value_text

                    # Write data immediately
                    writer.writerow(building_info)

                    # Save progress
                    save_last_processed_id(ad_id)

                    final_idx += 1

                except Exception as e:
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
    property_info(source_file_name)
