from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy

dropped_columns = [
    'date_game', 'age', 'team_id', 'game_location', 'opp_id', 'game_result', 'gs', 'reason'
]

dropped_columns_h = [
    'date_game', 'age', 'team_id', 'game_location', 'opp_id', 'game_result', 'gs'
]

int_stats = [
    'game_season', 'fg', 'fga', 'fg3', 'fg3a', 'ft', 'fta', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts', 'plus_minus'
]

float_stats = [
    'fg_pct', 'fg3_pct', 'ft_pct', 'game_score'
]

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
        
def time_to_decimal(time):

    split_time = time.split(':')
    mins = int(split_time[0])
    secs = int(split_time[1])
    return mins + secs/60.0

def scrape_gamelog(first_name, last_name, year):
    name = ""
    if len(last_name) < 5:
        name+=last_name[0:len(last_name)].lower()
    else:
        name+=last_name[0:5].lower()
    
    name+=first_name[0:2].lower()
    
    first_letter = last_name[0]

    url = f"https://www.basketball-reference.com/players/{first_letter}/{name}01/gamelog/{year}"
    response = requests.get(url)

    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': 'pgl_basic'})

        data = []

        if table:
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all('td')
                row_data = {}
                for cell in cells:
                    data_stat_value = cell.get('data-stat')
                    if data_stat_value:
                        value = cell.text.strip()
                        
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

            return df_gamelog
        else: 
            return
        
#print(scrape_gamelog("wilt", "chamberlain", 1970))