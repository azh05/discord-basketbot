import requests
import pandas as pd
import numpy as np
from historicaldata.gamelog import scrape_gamelog
import os
from google.cloud import storage
from dotenv import load_dotenv
import time

# first scrape nba website to get names of all players with more than 15 mpg (abritrary cutoff) of playing time
url = "https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2023-24&SeasonType=Regular%20Season&StatCategory=MIN"
r = requests.get(url).json()
table_headers = r['resultSet']['headers']

players = pd.DataFrame(r['resultSet']['rowSet'], columns=table_headers)
players.drop(columns=['RANK', 'TEAM_ID', 'PLAYER_ID'], inplace=True)
players.drop(players.columns.difference(['PLAYER', 'MIN']), axis=1, inplace=True)
players = players[players['MIN'] > 15]

list_of_players = list(players['PLAYER'])

# get gamelog for each player and save as csv
current_year = 2024

# upload csv to GCS (replace existing files with the same name)
def upload_csv(file_name):
    # get bucket_name and project_id from .env
    load_dotenv()
    bucket_name = os.getenv('bucket_name')
    project_id = os.getenv('project_id')

    # init client
    storage_client = storage.Client(project=project_id)

    # get bucket
    bucket = storage_client.bucket(bucket_name)

    # make blob to be stored in GCS
    blob = bucket.blob(file_name)

    # upload
    blob.upload_from_filename(file_name)


def add_to_gcs():
    i = 0
    for player in list_of_players:
        first_name, last_name = player.split(" ")
        df = scrape_gamelog(first_name=first_name, last_name=last_name, year=current_year)
        file_name = f"{first_name}_{last_name}.csv"
        
        if df is not None:
            df.to_csv(file_name, index=False)
        
        
        if os.path.exists(file_name) and i > 32:
            upload_csv(file_name)
            time.sleep(1)

        os.remove(file_name)
        i+=1

if __name__ == '__main__':
    add_to_gcs()