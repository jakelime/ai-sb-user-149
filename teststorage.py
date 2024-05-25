import numpy as np
import pandas as pd
from pathlib import Path

# from google.cloud import storage
from google.cloud import storage

# storage_client = storage.Client("ai-sandbox-company-25")
# df = pd.read_csv("https://storage.cloud.google.com/ppcs-datastore/db/db-manpower.csv")
df = pd.read_csv("gs://ppcs-datastore/db/db-manpower.csv")
print(df)


def upload_blob(
    source_file_name, destination_blob_name, bucket_name: str = "ppcs-datastore"
):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


# Example usage:
fname = "dummyfile.csv"
fpath = Path.cwd() / fname
db_file = df.to_csv(fpath)
upload_blob(fpath.name, fpath.name)
