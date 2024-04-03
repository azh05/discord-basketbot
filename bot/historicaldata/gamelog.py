from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import time
import unidecode
import re

dropped_columns = [
    'age', 'team_id', 'game_location', 'opp_id', 'game_result', 'gs', 'reason'
]

dropped_columns_h = [
    'age', 'team_id', 'game_location', 'opp_id', 'game_result', 'gs'
]

int_stats = [
    'game_season', 'fg', 'fga', 'fg3', 'fg3a', 'ft', 'fta', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts', 'plus_minus'
]

float_stats = [
    'fg_pct', 'fg3_pct', 'ft_pct', 'game_score'
]

fantasy_pts = {
    'fg': 1,
    'fga': -1,
    'ft': 1,
    'fta': -1,
    'ast': 2,
    'trb': 1,
    'stl': 4,
    'blk': 4,
    'tov': -2,
    'fg3': 1,
    'pts': 1
}

# calculate fantasy points from a game (espn fantasy points)
def calc_fantasy(df):
    fpoints = 0
    for stat in df.index:
        if stat in fantasy_pts:
            fpoints += int(df[stat]) * int(fantasy_pts[stat])

    return fpoints

# make plus minus a numeric
def process_pm(plus_minus):
    if not plus_minus:
        return None
    
    isMinus = False
    if '-' in plus_minus:
        isMinus = True
    
    value = plus_minus[1:]
    if not value:
        return None
    
    value = int(value)

    if isMinus:
        value *= -1
    
    return value
        
# make minutes played a numeric
def time_to_decimal(time):

    split_time = time.split(':')
    mins = int(split_time[0])
    secs = int(split_time[1])
    return mins + secs/60.0

# strip nonalphanumeric characters from a string (d'angelo russell --> dangelo russell)
def strip_non_alphanumeric(s):
    pattern = re.compile(r'[\W_]+')
    return pattern.sub('', s)

# scrape gamelog from basketball reference
def scrape_gamelog(first_name, last_name, year):
    name = ""

    # preprocess names
    first_name_stripped = strip_non_alphanumeric(first_name)
    last_name_stripped = strip_non_alphanumeric(last_name)

    if len(last_name_stripped) < 5:
        name+=last_name_stripped[0:len(last_name_stripped)].lower()
    else:
        name+=last_name_stripped[0:5].lower()

    name+=first_name_stripped[0:2].lower()
    
    first_letter = last_name_stripped[0].lower()

    url = f"https://www.basketball-reference.com/players/{first_letter}/{name}01/gamelog/{year}"
    response = requests.get(url)

    # to delay web scraping
    sleep_time = 3
    times_tried = 1

    while response.status_code != 200 and times_tried < 5:
        time.sleep(sleep_time*times_tried)
        response = requests.get(url)
        print(f'Try {times_tried}, status code {response.status_code}')
        times_tried += 1

    if response.status_code == 200:
        # create soup object
        soup = BeautifulSoup(response.text, 'html.parser')

        # check if the player in the link is the right player (antonio davis (01) vs anthony davis (02))
        title = unidecode.unidecode(soup.title.get_text())
        iteration = 2
        print(url)

        while title is not None and not (first_name.lower() in title.lower() and last_name.lower() in title.lower()) and iteration <= 7:
            url = f"https://www.basketball-reference.com/players/{first_letter}/{name}0{iteration}/gamelog/{year}"
            response = requests.get(url)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            title = unidecode.unidecode(soup.title.get_text())
            time.sleep(1)
            iteration += 1
    
        # find html attribute with id "pgl_basic"
        table = soup.find('table', {'id': 'pgl_basic'})

        data = []

        if table:
            rows = table.find_all("tr")
            
            # iterate through table rows
            for row in rows:
                
                # iterate through table data
                tds = row.find_all('td')
                row_data = {}
                for td in tds:

                    # get the type of stat in the td
                    data_stat_value = td.get('data-stat')

                    # if data_stat_value is not empty
                    if data_stat_value:

                        # get the value of the stat
                        value = td.text.strip()
                        
                        if data_stat_value == 'mp':
                            value = time_to_decimal(value)

                        elif data_stat_value in float_stats and value != '':
                            value = float(value)
                        
                        elif data_stat_value == 'plus_minus':
                            value = process_pm(value)
                        
                        row_data[data_stat_value] = value
                data.append(row_data)
        
            df_gamelog = pd.DataFrame(data)

            if 'reason' in df_gamelog.columns:
                df_gamelog.drop(columns=dropped_columns, inplace=True)
            else: 
                df_gamelog.drop(columns=dropped_columns_h, inplace=True)

            # clean dataframe and change datatypes

            historical_stat_ignore = [value for value in int_stats if value in df_gamelog.columns]

            df_gamelog.reset_index(drop=True)
            df_gamelog.dropna(inplace=True)
            df_gamelog[historical_stat_ignore] = df_gamelog[historical_stat_ignore].apply(pd.to_numeric).astype('Int64')
            df_gamelog['ft_pct'] = pd.to_numeric(df_gamelog['ft_pct']).astype('float64')
            
            # change to datetime
            df_gamelog['date_game'] = pd.to_datetime(df_gamelog["date_game"], format='%Y-%m-%d')

            # add fantasy points
            df_gamelog['fpoints'] = df_gamelog.apply(calc_fantasy, axis=1)

            return df_gamelog
        else:
            return
    else: 
        print("Could not access link")

# Tests    

if __name__ == '__main__': 
    df = scrape_gamelog("jayson", "tatum", 2024)
    print(df)