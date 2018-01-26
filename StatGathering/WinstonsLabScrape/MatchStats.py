''' This file holds any functions that can be used to
    gather individual match data.'''

#Imports
import time
import requests
from copy import deepcopy
from pprint import pprint
from selenium import webdriver
from bs4 import BeautifulSoup
from dateutil.parser import parse
import pandas as pd
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Global variables
MATCH_LIST_URL = "https://www.winstonslab.com/events/event.php?id=86#matches"
BASE_MATCH_URL = "https://www.winstonslab.com/matches/match.php"
WEB_DRIVER_LOC = "/Applications/chromedriver"
MAP_TYPE_DICT = {
    "KOTH" : ["Ilios", "Lijiang Tower",
            "Nepal","Oasis"],
    "Assault": ["Hanamura", "Horizon Lunar Colony",
              "Temple of Anubis", "Volskaya Industries"],
    "Escort" : ["Dorado", "Junkertown",
             "Route 66", "Watchpoint: Gibraltar"],
    "Hybrid" : ["Blizzard World", "Eichenwalde",
             "Hollywood", "King's Row", "Numbani"]
}

# function for grabbing detailed match data from a particular match
def get_detailed_match_data(game_id):
    '''
    Gets detailed match stats.

    Args:
        game_id: str
            This is the id given to the match by winstons lab.

    Returns:
        pandas dataframe
    '''

    # Create match url
    full_url = "{}?id={}".format(BASE_MATCH_URL, game_id)


    # Set up webdriver
    # TODO: Wrap this in a try except clause
    driver = webdriver.Chrome(WEB_DRIVER_LOC)
    driver.get(full_url)
    time.sleep(10) #This should be replaced with something listening for the page to load
  

    # Click button to show the detailed stats
    detail_button = driver.find_element_by_class_name("showDetailedStatsBut")
    #print(detail_button.text)
    detail_button.click()
    time.sleep(10)

    # Create Beautiful Soup object from the div containing the table
    page_source = driver.page_source
    driver.close()
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
    header_list = ["Match ID"]
    for header in header_elems:
        header_list.append(header.text)
    #pprint(header_list)
    

    row_list = table_data.findAll("tr")
    stat_list = []
    for row in row_list:
        this_row = [game_id]
        elems = row.findAll("td")
        #print("-----------------------")
        for i, item in enumerate(elems[0:]):
            this_row.append(item.text.strip())
            #print("{}: {}".format(header_list[i], item.text.strip()))
        #print(this_row)
        stat_list.append(this_row)

    df = pd.DataFrame(stat_list, columns=header_list)
    #print(df.head())

    return df


def get_map_summary_data(game_id):
    '''
    Gets the date, teams and winner of each map in a given match.

    Args:
        game_id: str
            This is the id given to the match by winstons lab.

    Returns:
        pandas dataframe
    '''

    # Create match url
    full_url = "{}?id={}".format(BASE_MATCH_URL, game_id)

    # get html from match page
    response = requests.get(full_url)
    html = BeautifulSoup(response.text, "lxml")
    
    # build match info shared by all maps
    map_base = {"Match Id" : game_id}
    logging.debug("mapbase = {}".format(map_base))

    # get date
    date_str = html.find("span", {"id": "tzDate_1"}).text
    date_list = date_str.split(" ")
    day = date_list[0].split("t")[0]
    month = date_list[2]
    year = date_list[3]
    match_date = parse("{} {} {}".format(day, month, year))
    map_base["Date"] = match_date.date().isoformat()
    logging.debug("mapbase = {}".format(map_base))

    # get divs for all other data
    score_divs = html.find("div", {"class": "mini-map-scores"}).label.findAll("div", recursive=False)

    # set team names
    team_names = score_divs[0].findAll("div") 
    map_base["Team A"] = team_names[0].text
    map_base["Team B"] = team_names[1].text
    logging.debug("mapbase = {}".format(map_base))

    # get score divs
    map_scores = score_divs[1:]

    # list to collect map dicts
    map_dict_list = []

    #loop through maps
    for m in map_scores:
        mp = deepcopy(map_base) 
        
        map_details = m.findAll("div", recursive=False)

        # Get map name
        mp["Map Name"] = map_details[0]['title']

        # Get map type
        for key, val in MAP_TYPE_DICT.items():
            if mp["Map Name"] in val:
                mp["Map Type"] = key

        # Get result
        if 'winner' in map_details[1]["class"]:
            mp["Winner"] = "Team A"
        elif 'loser' in map_details[1]["class"]:
            mp["Winner"] = "Team B"
        else:
            mp["Winner"] = "Tie"

        logging.debug("mp={}".format(mp))
        map_dict_list.append(mp)


    return pd.DataFrame.from_records(map_dict_list)
















if __name__ == "__main__":
    df = detailed_match_data("2367")
    print(df.head())
    print(df.tail())
    print(df.shape)
