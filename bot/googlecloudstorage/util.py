import requests
import pandas as pd

def name_to_file_name(name):
    names = name.split(" ") # gets first name, last name, (opt III, Jr, Sr)

    first_name = names[0]
    last_name = names[1]
    if len(names) == 3:
        last_name += f" {names[2]}"

    return f"{first_name}_{last_name}.csv"


def file_name_to_names(file_name):
    names = file_name.split("_")

    return names[0], names[1]


# first scrape nba website to get names of all players with more than 15 mpg (abritrary cutoff) of playing time
def get_list_of_players():
    url = "https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2023-24&SeasonType=Regular%20Season&StatCategory=MIN"
    r = requests.get(url).json()
    table_headers = r['resultSet']['headers']

    players = pd.DataFrame(r['resultSet']['rowSet'], columns=table_headers)
    players.drop(columns=['RANK', 'TEAM_ID', 'PLAYER_ID'], inplace=True)
    players.drop(players.columns.difference(['PLAYER', 'MIN']), axis=1, inplace=True)
    players = players[players['MIN'] > 15]

    list_of_players = list(players['PLAYER'])

    return list_of_players