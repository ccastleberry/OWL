''' This file holds any functions that can be used to
    gather individual match data.'''

#Imports
import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from pprint import pprint

# Global variables
MATCH_LIST_URL = "https://www.winstonslab.com/events/event.php?id=86#matches"
BASE_MATCH_URL = "https://www.winstonslab.com/matches/match.php"
WEB_DRIVER_LOC = "/Applications/chromedriver"

# function for grabbing detailed match data from a particular match
def detailed_match_data(game_id):
    '''
    Gets detailed match stats.

    Args:
        game_id: str
            This is the id given to the match by winstons lab.

    Returns:
        String in csv format with headers
    '''

    # Create match url
    full_url = "{}?id={}".format(BASE_MATCH_URL, game_id)


    # Set up webdriver
    # TODO: Wrap this in a try except clause
    driver = webdriver.Chrome(WEB_DRIVER_LOC)
    driver.get(full_url)
    time.sleep(5) #This should be replaced with something listening for the page to load
  


    # Click button to show the detailed stats
    detail_button = driver.find_element_by_class_name("showDetailedStatsBut")
    detail_button.click()

    # Create Beautiful Soup object from the div containing the table
    page_source = driver.page_source
    new_html = BeautifulSoup(page_source, "lxml")

    # Grab just the table
    div = new_html.findAll("div", {"class": "side-by-side-stats"})[0]
    detail = div.findAll("div", recursive=False)[2]
    stat_table = detail.table


    # split the table into headers and body
    table_headers = stat_table.thead
    table_data = stat_table.tbody

    # create a list of headers
    header_elems = table_headers.findAll("th")
    header_list = []
    for header in header_elems:
        header_list.append(header.text)
        pprint(header_list)

    row_list = table_data.findAll("tr")
    for row in row_list[0:3]:
        elems = row.findAll("td")
        print("-----------------------")
        for i, item in enumerate(elems[0:]):
            print("{}: {}".format(header_list[i], item.text.strip()))