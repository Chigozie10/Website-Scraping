# Importing the necessary libraries such as selenium to get the data from a dynamic site

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
import pandas as pd
errors = []
season = []
# print(season)

for id in range(46605, 46985):
    # This is the targeted url I am scraping for data
    my_url = f'https://www.premierleague.com/match/{id}'

    # This is to initialize option to avoid the chrome browser from popping up
    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    # This is to direct the web driver on the location of the chrome driver executable
    # driver = webdriver.Chrome("/Users/AgbaneloChigozie/opt/anaconda3/lib/python3.9/site-packages/selenium/webdriver/chrome/chromedriver",options=option)

    # This is to install the chrome driver whenever it is needed by the script
    # the options part is to prevent the driver from automatically popping up the chrome browser
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

    # This gets the targetted url data
    driver.get(my_url)

    # print(driver)

    try:


        # This is to get the date from the url website
        date = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((
        By.XPATH, '//*[@id="mainContent"]/div/section/div[2]/section/div[1]/div/div[1]/div[1]'))).text

        # This is to convert the date form to month/day/year
        date = datetime.strptime(date, '%a %d %b %Y').strftime('%m/%d/%Y')

        # This is to get the home team
        home_team = driver.find_element("xpath", '//*[@id="mainContent"]/div/section/div[2]/section/div[3]/div/div/div[1]/div[1]/a[2]/span[1]').text

        # This is to get the away team
        away_team = driver.find_element("xpath", '//*[@id="mainContent"]/div/section/div[2]/section/div[3]/div/div/div[1]/div[3]/a[2]/span[1]').text

        # Printing the results
        # print(date)
        # print(home_team)
        # print(away_team)

        scores = driver.find_element("xpath", '//*[@id="mainContent"]/div/section/div[2]/section/div[3]/div/div/div[1]/div[2]/div/div').text
        home_score = scores.split('-')[0]
        away_score = scores.split('-')[1]

        if home_score == away_score:
            home_team_result = "D"
            away_team_result = "D"
        elif home_score > away_score:
            home_team_result = "W"
            away_team_result = "L"
        else:
            home_team_result = "L"
            away_team_result = "W"

        # printing the results
        # print(home_score)
        # print(away_score)

        elem = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//ul[@class='tablist']//li[@data-tab-index='2']")))
        elem.click()
        sleep(5)

        dfs = pd.read_html(driver.page_source)
        stats = dfs[-1]
        print(stats)

        # quit the driver
        driver.quit()

    except:
        driver.quit()
        errors.append(id)
        continue


    # Handling the stats
    home_stats = {}
    away_stats = {}

    home_series = stats[home_team]
    away_series = stats[away_team]
    stats_series = stats['Unnamed: 1']

    for row in zip(home_series, stats_series, away_series):
        stat = row[1].replace(' ', '_').lower()
        home_stats[stat] = row[0]
        away_stats[stat] = row[2]

    stats_check = ['possession_%', 'shots_on_target', 'shots', 'touches', 'passes',
                'tackles', 'clearances', 'corners', 'offsides', 'yellow_cards',
                'red_cards', 'fouls_conceded']

    for stat in stats_check:
        if stat not in home_stats.keys():
            home_stats[stat] = 0
            away_stats[stat] = 0

    # print(home_stats)

    # storing the data
    match = [date, home_team, away_team, home_score, away_score, home_team_result, away_team_result, home_stats['possession_%'], away_stats['possession_%'],
                home_stats['shots_on_target'], away_stats['shots_on_target'], home_stats['shots'], away_stats['shots'],
                home_stats['touches'], away_stats['touches'], home_stats['passes'], away_stats['passes'],
                home_stats['tackles'], away_stats['tackles'], home_stats['clearances'], away_stats['clearances'],
                home_stats['corners'], away_stats['corners'], home_stats['offsides'], away_stats['offsides'],
                home_stats['yellow_cards'], away_stats['yellow_cards'], home_stats['red_cards'], away_stats['red_cards'],
                home_stats['fouls_conceded'], away_stats['fouls_conceded']]

    season.append(match)

    # print(season)

    print(f'ID {id} scraped.')

# Exporting the data

columns = ['date', 'home_team', 'away_team', 'home_score', 'away_score', 'home_team_result', 'away_team_result']

for stat in stats_check:
    columns.append(f'home_{stat}')
    columns.append(f'away_{stat}')

dataset = pd.DataFrame(season, columns=columns)
dataset.to_csv('Premier_league_19_20.csv', index=False)









# for id in range(46605, 46985):
#     my_url = f'https://www.premierleague.com/match/{id}'
#     option = Options()
#     option.headless = True
#     driver = webdriver.Chrome(options=option)
#     driver.get(my_url)