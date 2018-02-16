'''Collection of functions that scrape the overwatch league site.

Created: 2018-02-15
Created By: Caleb Castleberry (castle.caleb@gmail.com)
Last Updated: 2018-02-15
Updated By: Caleb Castleberry (castle.caleb@gmail.com)
'''

# Imports
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from pprint import pprint


def get_hero_info():
    ''' Get a list of heroes and their classifications.
    
    Returns:
        pandas dataframe
    '''
    # Get page and create BS object
    url = 'https://playoverwatch.com/en-us/heroes/'
    r = requests.get(url)
    bsobj = BeautifulSoup(r.text, 'lxml')

    # Start parsing the page
    hero_containers = bsobj.findAll('div', 
        {'class': 'hero-portrait-detailed-container'})
    
    # initialize dict to hold heros
    hero_list = []

    # loop through containers
    for container in hero_containers:
        hero_dict = {}
        hero_dict['Hero Name'] = container.a.text
        hero_dict['Hero Category'] = container.attrs['data-groups'][2:-2].title()
        hero_list.append(hero_dict)
    
    hero_df = pd.DataFrame(hero_list)

    return hero_df


def get_map_info():
    '''Gets a list of maps and their category

    Returns:
        pandas dataframe
    '''

    # Get page and create BS object
    url = 'https://playoverwatch.com/en-us/game/overview/#maps-section'
    r = requests.get(url)
    bsobj = BeautifulSoup(r.text, 'lxml')

    # Get containers
    map_containers = bsobj.findAll('div', 
        {'data-js': 'map'})
    
    map_list = []

    for container in map_containers:
        map_dict = {}
        map_dict['Map Name'] = container.attrs['data-name']
        map_dict['Map Category'] = container.findAll('div', 
            recursive=False)[1].div.findAll('span')[1].text
        map_list.append(map_dict)
    
    map_df = pd.DataFrame(map_list)

    return map_df


def get_team_info():
    '''Gets a list of teams and their location

    Returns:
        pandas dataframe
    '''

    player_df = get_player_info()
    team_abbr_df = player_df[['Team Abbr', 'Team Name']].drop_duplicates()

    # Get page and create BS object
    url = "https://overwatchleague.com/en-us/teams"
    
    # Create headless chrome webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1200x600')

    driver = webdriver.Chrome('/Applications/chromedriver',
        chrome_options=options)

    # Get page and give it time to load
    driver.get(url)
    driver.implicitly_wait(10)

    bsobj = BeautifulSoup(driver.page_source, 'lxml')
    driver.close()

    # get containers
    team_containers = bsobj.findAll('div',
        {'class': 'Card--team'})

    
    team_list = []

    for container in team_containers:
        team_dict = {}
        name = container.find('h2').text
        team_dict['Team Name'] = name
        team_dict['Team Location'] = container.find('p').text
        abbr = team_abbr_df[team_abbr_df['Team Name'] == name].iloc[0]['Team Abbr']
        team_dict['Team Abbr'] = abbr
        team_list.append(team_dict)

    team_df = pd.DataFrame(team_list)

    return team_df


def get_player_info():
    ''' Gets a list of players and basic stats about them

    Returns:
        pandas dataframe
    '''

    # get page
    url = "https://overwatchleague.com/en-us/players"
    r = requests.get(url)
    bsobj = BeautifulSoup(r.text, 'lxml')

    # get list of players
    player_containers = bsobj.table.findAll('tr')

    player_list = []

    for player in player_containers[1:]:
        player_dict = {}

        data = player.findAll('td')
        player_dict['Tag'] = data[0].b.text
        player_dict['First Name'] = data[1].text
        player_dict['Last Name'] = data[2].text
        hometown = data[3].text
        player_dict['Home Country'] = hometown.split(',')[-1]
        player_dict['Home City'] = hometown[:-4]
        player_dict['Team Name'] = data[4].findAll('b')[0].text
        player_dict['Team Abbr'] = data[4].findAll('b')[1].text
        player_dict['Role'] = data[5].text

        player_list.append(player_dict)
    
    player_df = pd.DataFrame(player_list)

    return player_df




if __name__ == "__main__":
    #pprint(get_hero_info().head())
    #pprint(get_map_info().head())
    #pprint(get_team_info().head())
    #pprint(get_player_info().head())

