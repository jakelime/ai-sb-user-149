from pathlib import Path

import pandas as pd

try:
    import storage
except ImportError:
    from ppcs import storage


def test_gcs_push_file_to_liveschedule():
    db = storage.DatabaseManager()
    df = pd.read_csv("gs://ppcs-datastore/dummyfile.csv")
    # logger.info(df)
    with storage.LocalTempFolder(remove_temp_files=True) as temp_dir:
        temp_dir = Path(temp_dir)
        fname = "dummy3.csv"
        fpath = temp_dir / fname
        df.to_csv(fpath)
        db.upload_to_gcs_bucket(str(fpath.absolute()), f"live_schedule/{fpath.name}")


def main():
    test_gcs_push_file_to_liveschedule()


if __name__ == "__main__":
    main()
