from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import re
import csv

search = input("What is the item you are looking for? ")

URL = ("https://google.com")
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.get(URL)

driver.find_element(By.CLASS_NAME, "gLFyf").send_keys(f"{search}", Keys.RETURN)
time.sleep(2)

item_found = False
for n in range(1, 2):
    # footer = driver.find_element(By.TAG_NAME, "footer")
    # delta_y = int(footer.rect['y'])
    ActionChains(driver) \
        .scroll_by_amount(0, 500) \
        .perform()

while not item_found:
    item_list = driver.find_element(By.CSS_SELECTOR, "#search .dURPMd")
    title_list = item_list.find_elements(By.CLASS_NAME, "h3")
    link_list = item_list.find_elements(By.TAG_NAME, "a")
    price_list = item_list.find_elements(By.CLASS_NAME, "ChPIuf")

    short_info = ""
    for title in title_list:
        print(title.text)
        short_info = title.text
    if short_info != "":
        item_found = True
        break

        link = item.find_element(By.TAG_NAME, "a")
        link.click()

    img = driver.find_element(By.CSS_SELECTOR, ".img_container a img")
    print(img.text)