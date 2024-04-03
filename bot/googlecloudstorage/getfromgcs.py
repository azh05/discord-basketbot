from google.cloud import storage
import pandas as pd
from dotenv import load_dotenv
from bot.googlecloudstorage.util import name_to_file_name
import os
import io

def get_dataframe(name): 
    load_dotenv()
    bucket_name = os.getenv('bucket_name')
    project_id = os.getenv('project_id')

    storage_client = storage.Client(project=project_id)

    bucket = storage_client.bucket(bucket_name=bucket_name)

    file_name = name_to_file_name(name)

    blob = bucket.blob(blob_name=file_name)

    # Download the CSV file as bytes
    csv_bytes = blob.download_as_string()

    # Convert the bytes to a Pandas DataFrame
    df = pd.read_csv(io.BytesIO(csv_bytes))

    return df

if __name__ == '__main__':
    print(get_dataframe("Jayson Tatum"))