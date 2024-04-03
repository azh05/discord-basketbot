import requests
import pandas as pd
import numpy as np
from bot.historicaldata.gamelog import scrape_gamelog
import os
from google.cloud import storage
from dotenv import load_dotenv
import time
from bot.googlecloudstorage.util import name_to_file_name, get_list_of_players

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
    list_of_players = get_list_of_players()
    players_not_added = []
    for player in list_of_players:
        names = player.split(" ") # gets first name, last name, (opt III, Jr, Sr)

        first_name = names[0]
        last_name = names[1]
        if len(names) == 3:
            last_name += f" {names[2]}"
            
        file_name = name_to_file_name(player)

        print(f"Processing {player}")
        df = scrape_gamelog(first_name=first_name, last_name=last_name, year=current_year)

        if df is not None:
            df.to_csv(file_name, index=False)
        else:
            players_not_added.append(player)
        
        if os.path.exists(file_name):
            upload_csv(file_name)
            time.sleep(3)
            os.remove(file_name)

    print(players_not_added) # clint capela, cedi osman not added

if __name__ == '__main__':
    add_to_gcs()