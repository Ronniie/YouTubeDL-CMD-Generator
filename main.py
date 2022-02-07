# YouTubeDL-CMD-Generator - Generates a command line for youtube-dl
# It will scrape a specific URL and generate a command line for youtube-dl
import os
from bs4 import BeautifulSoup
import chromedriver_binary  # pip3 install chromedriver-binary==your_version in chrome://settings/help
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

opts = Options()
opts.add_argument('--headless')

def get_soup(URL, xpath):
    driver = webdriver.Chrome(options=opts)
    driver.get(URL)
    try:
        WebDriverWait(driver, 60).until(lambda driver: driver.find_element(By.XPATH, xpath))
    except:
        print("Error: No results found")
        driver.quit()
        exit()
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    return soup



while True:
    print("Please enter the URL")
    URL = input()
    if URL == "":
        print("Invalid URL")
        continue
    else:
        break

soup = get_soup(URL, '//*[@id="list"]/a')
query = soup.find_all("div", {"class": "list-group text-break"})

query_list = []
for i in query:
    for j in i.find_all("a"):
        query_list.append(j.text.strip())
        print(f"{query_list.index(j.text.strip())}) {j.text}")

while True:
    print("Select the content:")
    select = int(input())
    if select < 0 or select > len(query_list):
        print("Invalid Selection, please enter a valid selection")
        continue
    else:
        break

selection = query_list[select].replace(" ", "%20")
soup = get_soup(
    f"{URL}{query_list[select].replace(' ', '%20')}/",
    '//*[@id="list"]/div/a'
)
query = soup.find_all("div", {"class": "list-group text-break"})

video_list = []
for i in query:
    for j in i.find_all("a"):
        if j.text.strip() == "":
            pass
        else:
            url = f"{URL}/{selection}/{j.text.strip().replace(' ', '%20')}?a=view"
            print(f"Grabbing {j.text.strip()}...")
            soup = get_soup(url, '//*[@id="dlurl"]')
            query = soup.find("input", {"id": "dlurl"})
            video_list.append(query["value"])
            print(f"{video_list.index(query['value'])}) Adding {j.text.strip()} to list...")

with open("urls.txt", "w") as f:
    if os.stat("urls.txt").st_size != 0:
        f.truncate()

    for i in video_list:
        f.write(f'youtube-dl "{i}"') if i == video_list[-1] else f.write(f'youtube-dl "{i}" && ')