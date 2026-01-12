#!/usr/bin/env python3
from bs4 import BeautifulSoup
import datetime
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# TODO - 1234.MN COURSE LIST SCRAPING USING BEAUTIFUL SOUP AND SELENIUM

main_url = "http://1234.mn/course"

# Create empty lists for collecting data
course_list = []
today = datetime.date.today().strftime("%Y%m%d")

# File names
file_name = f"../output/course_list_{today}.csv"

def course_finder():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome()  # Make sure you have the appropriate WebDriver installed
    driver.get(main_url)

    try:
        # Wait for the page to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "span12")))

        # Scroll to the bottom of the page
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for new content to load
            time.sleep(2)  # Adjust sleep time if necessary

            # Calculate new scroll height and compare with last height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # Exit the loop if no new content is loaded
            last_height = new_height

        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        div_elements = soup.find(id="content").find_all("div")
        main_element = div_elements[3].find(class_="span12")

        if not main_element:
            print("Main element not found. Exiting...")
            return

        courses = main_element.find_all("div", class_="span3")
        if not courses:
            print("No courses found.")
            return

        for course in courses:
            try:
                course_name = course.find("p").find("a").text.strip() if course.find("p") else "N/A"
                link = course.find("a").get("href") if course.find("a") else None
                course_link = link if link else "N/A"

                # This is the p element that contains lot of stuff.
                video_count = (
                    course.find(class_="blog-post-title")
                    .find("p")
                    .find("i", class_="ifc-video_camera").next_sibling.strip()
                    if course.find(class_="blog-post-title")
                    and course.find(class_="blog-post-title").find("p")
                    and course.find(class_="blog-post-title").find("p").find(class_="ifc-video_camera")
                    else "0"
                )
                duration = (
                    course.find(class_="blog-post-title")
                    .find("p")
                    .find("i", class_="ifc-clock").next_sibling.strip()
                    if course.find(class_="blog-post-title")
                    and course.find(class_="blog-post-title").find("p")
                    and course.find(class_="blog-post-title").find("p").find(class_="ifc-clock")
                    else "N/A"
                )
                views = course.find("i", class_="ifc-play").next_sibling.strip() if course.find(class_="ifc-play") else "0"
                enrolled = course.find("i", class_="ifc-student").next_sibling.strip() if course.find(class_="ifc-student") else "0"
                p_elements = course.find(class_="blog-post-title").find_all("p") if course.find(class_="blog-post-title") else []
                new_price = "N/A"
                old_price = "N/A"
                if len(p_elements) >= 3:
                    span_elements = p_elements[2].find_all("span")
                    if len(span_elements) >= 3:
                        new_price = span_elements[1].find("span").text.strip() if span_elements[1].find("span") else "N/A"
                        old_price = span_elements[2].text.strip()

                course_dict = {
                    "id": len(course_list) + 1,
                    "course_name": course_name,
                    "video_count": video_count,
                    "duration": duration,
                    "course_link": f"http://1234.mn{course_link}",
                    "views": views,
                    "enrolled": enrolled,
                    "old_price": old_price,
                    "new_price": new_price,
                }
                course_list.append(course_dict)

            except AttributeError as e:
                print(f"Error processing course: {e}. Skipping...")

        # Write to CSV if courses exist
        if course_list:
            with open(file_name, mode="w", newline="", encoding="utf-8") as file:
                fieldnames = course_list[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(course_list)
            print(f"Data written to {file_name}")
        else:
            print("No course data to write.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    course_finder()
