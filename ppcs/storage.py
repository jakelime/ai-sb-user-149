import shutil
from io import BytesIO
from pathlib import Path

import pandas as pd
from google.cloud import storage

try:
    import utils
except ImportError:
    from ppcs import utils


APP_NAME = "ppcs"
logger = utils.init_logger(APP_NAME)


class LocalTempFolder:
    remove_temp_files: bool = True

    def __init__(self, remove_temp_files: bool = True):
        self.remove_temp_files = remove_temp_files

    def __enter__(self):
        self.temp_dir = Path.cwd() / "tempdir"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        return self.temp_dir

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.remove_temp_files:
            shutil.rmtree(self.temp_dir)


class DatabaseManager:
    def __init__(
        self,
        project_name: str = "ai-sandbox-company-25",
        bucket_name: str = "ppcs-datastore",
        db_manpower: str = "gs://ppcs-datastore/db/db-manpower.csv",
        db_shopfloor: str = "gs://ppcs-datastore/db/db-shopfloor.csv",
        live_schedule_foldername: str = "live_schedule",
        input_jobs: str = "gs://ppcs-datastore/input_files/data_input-job_delivery_dates.csv",
        input_workscope: str = "gs://ppcs-datastore/input_files/data_input-jobs_workscope.csv",
        shift_table: str = "gs://ppcs-datastore/db/shift_table.csv",
    ):
        self.bucket_name = bucket_name
        self.db_manpower = db_manpower
        self.db_shopfloor = db_shopfloor
        self.live_schedule_foldername = live_schedule_foldername
        self.input_jobs = input_jobs
        self.input_workscope = input_workscope
        self.shift_table = shift_table
        self.storage_client = storage.Client(project_name)
        self.bucket = self.storage_client.get_bucket(bucket_name)

    def get_dataframe(self, storage_address: str) -> pd.DataFrame:
        return pd.read_csv(storage_address)

    def get_df_shopfloor(self) -> pd.DataFrame:
        return self.get_dataframe(self.db_shopfloor)

    def get_df_manpower(self) -> pd.DataFrame:
        return self.get_dataframe(self.db_manpower)

    def get_shift_table(self) -> pd.DataFrame:
        return self.get_dataframe(self.shift_table)

    def get_df_liveschedule(self) -> pd.DataFrame:
        """
        The latest liveschedule is the last file in the folder.
        Retrieves the last file in the folder, return as a dataframe

        :return: liveschedule
        :rtype: pd.DataFrame
        """
        blobs = self.get_liveschedule_files()
        blob_contents = blobs[-1].download_as_bytes()
        df = pd.read_csv(BytesIO(blob_contents))
        return df

    def get_liveschedule_files(self) -> list:
        blobs = list(
            self.storage_client.list_blobs(
                self.bucket_name, prefix=self.live_schedule_foldername
            )
        )
        return sorted(blobs, key=lambda blob: blob.time_created)

    def get_df_input_jobs(self) -> pd.DataFrame:
        return self.get_dataframe(self.input_jobs)

    def get_df_input_workscope(self) -> pd.DataFrame:
        return self.get_dataframe(self.input_workscope)

    def upload_to_gcs_bucket(self, src_filename, dst_filename):
        """Uploads a file to the bucket."""
        blob = self.bucket.blob(dst_filename)
        blob.upload_from_filename(src_filename)
        logger.info(f"file {src_filename} uploaded to {dst_filename}.")


def main():
    db = DatabaseManager()
    db.get_df_liveschedule()


if __name__ == "__main__":
    main()
