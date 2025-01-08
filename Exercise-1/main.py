import os
import requests
import zipfile
import logging

logging.basicConfig(level=logging.INFO)

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_PATH = os.path.join(BASE_PATH, "downloads")
CSV = ".csv"


def prepare_files_list(download_uris):
    return [{"zip": uri.split('/')[-1], "csv": uri.split('/')[-1].replace(".zip", ".csv")} for uri in download_uris]


def download_files(download_uris, files):
    if not os.path.exists(DOWNLOADS_PATH):
        os.mkdir(DOWNLOADS_PATH)
        logging.info("'downloads' folder created.")
    else:
        logging.info("'downloads' folder already exists.")

    for (uri, file_info) in zip(download_uris, files):
        response = requests.get(uri)
        if response.status_code != 200:
            logging.error(f"Failed to download file from: {uri}. Status code: {response.status_code}")
            continue
        
        with open(os.path.join(DOWNLOADS_PATH, file_info['zip']), "wb") as zip_file:
            zip_file.write(response.content)
            logging.info(f"file: '{uri.split('/')[-1]}' downloaded to 'downloads' folder.")


def extract_zip_file(files):
    for file_info in files:
        try:
            logging.info(f"Extracting file: '{file_info['csv']}' from '{file_info['zip']}' to 'downloads' folder.")
            with zipfile.ZipFile(os.path.join(DOWNLOADS_PATH, file_info['zip']), 'r') as zip_file:
                zip_file.extract(file_info['csv'], DOWNLOADS_PATH)

        except zipfile.BadZipFile:
            logging.error(f"Error occured when tried to unzip file: '{file_info['zip']}'")

        except FileNotFoundError:
            logging.error(f"File Not Found Error when tried to unzip file: '{file_info['zip']}'")


def delete_zip_files(files):
    for file_info in files:
        try:
            os.remove(os.path.join(DOWNLOADS_PATH, file_info['zip']))
            logging.info(f"file: '{file_info['zip']}' deleted from 'downloads' folder.")

        except FileNotFoundError:
            logging.error(f"File Not Found Error when tried to unzip file: '{file_info['zip']}'")


def main():

    download_uris = [
        "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
        "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
        "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
        "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
        "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
        "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
        "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
    ]

    files = prepare_files_list(download_uris)
    download_files(download_uris, files)
    extract_zip_file(files)
    delete_zip_files(files)


if __name__ == "__main__":
    main()
