# YouTubeDL-CMD-Generator - Generates a command line for youtube-dl
# It will scrape a specific URL and generate a command line for youtube-dl
import os

# BeautifulSoup
from bs4 import BeautifulSoup
import chromedriver_binary  # pip3 install chromedriver-binary==your_version in chrome://settings/help

# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

opts = Options()  # Create a new Chrome session
opts.add_argument('--headless')  # Runs Chrome in headless mode.
DIR_NAME = "Season"  # Season1
previous_source = False
source_input = True
source = ""

def get_soup(url, xpath):
    """
    Gets the soup object from the url
    :param url:
    :param xpath:
    :return:
    """
    # Create a new Chrome session
    driver = webdriver.Chrome(options=opts)
    # Load the page
    driver.get(url)
    try:  # Wait for the page to load
        WebDriverWait(driver, 60).until(lambda d: d.find_element(By.XPATH, xpath))
    except:  # If it fails, return None
        print("Error: No results found")
        driver.quit()
        exit()

    # Get the page source and create a soup object
    html = BeautifulSoup(driver.page_source, "html.parser")
    # Close the browser
    driver.quit()
    # Return the soup object
    return html


while True:
    if previous_source:
        source_input = False
        source = previous_source
    else:
        pass
    while source_input:
        """
        Main loop
        Enter the URL
        """
        source = input("Enter the URL: ")

        if source == "":
            print("Error: No URL entered")
            continue
        else:
            source_input = False

    soup = get_soup(source, '//*[@id="list"]/a')
    query = soup.find_all("div", {"class": "list-group text-break"})

    query_list = []
    for i in query:
        for j in i.find_all("a"):
            query_list.append(j.text.strip())
            print(f"{query_list.index(j.text.strip())}) {j.text}")

    while True:
        select = int(input("Select the content: "))
        if select < 0 or select > len(query_list):
            print("Invalid Selection, please enter a valid selection")
            continue
        else:
            break

    selection = query_list[select].replace(" ", "%20")  # Replace spaces with %20
    soup = get_soup(
        f"{source}{query_list[select].replace(' ', '%20')}/",  # URL
        '//*[@id="list"]/div/a'  # XPath
    )  # Get the soup object
    query = soup.find_all("div", {"class": "list-group text-break"})  # Get the list of episodes from the soup object

    video_list = []  # List of videos
    for i in query:
        for j in i.find_all("a"):  # Get the links from the soup object
            if j.text.strip() == "":  # If the link is empty, skip it
                pass
            else:  # If the link is not empty, add it to the list
                url = f"{source}/{selection}/{j.text.strip().replace(' ', '%20')}?a=view"  # URL
                print(f"Grabbing {j.text.strip()}...")  # Print the video name
                soup = get_soup(url, '//*[@id="dlurl"]')  # Get the soup object
                query = soup.find("input", {"id": "dlurl"})  # Get the link from the soup object
                video_list.append(query["value"])  # Add the link to the list
                print(f"{video_list.index(query['value'])}) Adding {j.text.strip()} to list...")  # Print the video name

    with open("urls.txt", "a+") as f:  # Open the file
        # Check if previous_source exists
        if previous_source:
            for i in video_list:
                f.write(f'youtube-dl "{i}"') if i == video_list[-1] else f.write(
                    f'youtube-dl "{i}" && ')
        else:
            if os.stat("urls.txt").st_size != 0:  # If the file is not empty
                f.truncate()  # Clear the file

            for i in video_list:  # Write the commands to the file
                # If it is the last video, don't add the &&
                f.write(f'youtube-dl "{i}"') if i == video_list[-1] else f.write(f'youtube-dl "{i}" && ')

    print("Would you like to continue? (y/n) ")
    previous_source = source
    if input() == "n":
        break
    else:
        continue
