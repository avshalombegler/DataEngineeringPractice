import os
import requests
import zipfile
import logging
import validators

logging.basicConfig(level=logging.INFO)

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_PATH = os.path.join(BASE_PATH, "downloads")
CSV = ".csv"


def validate_uris(download_uris):
    for uri in download_uris:
        if not validators.url(uri):
            logging.warning(f"Invalid URL detected: {uri}")


def prepare_files_list(download_uris):
    return [{"zip": uri.split('/')[-1], "csv": uri.split('/')[-1].replace(".zip", ".csv")} for uri in download_uris]

def ensure_folder_exists():
    if not os.path.exists(DOWNLOADS_PATH):
        os.mkdir(DOWNLOADS_PATH)
        logging.info("'downloads' folder created.")
    else:
        logging.info("'downloads' folder already exists.")

def download_files(download_uris, file_mappings):
    ensure_folder_exists()
    for (uri, file_info) in zip(download_uris, file_mappings):
        response = requests.get(uri, timeout=10)
        if response.status_code != 200:
            logging.error(f"Failed to download file from: {uri}. Status code: {response.status_code}")
            continue
        
        with open(os.path.join(DOWNLOADS_PATH, file_info['zip']), "wb") as zip_file:
            zip_file.write(response.content)
            logging.info(f"file: '{uri.split('/')[-1]}' downloaded to 'downloads' folder.")


def extract_zip_file(file_mappings):
    for file_info in file_mappings:
        try:
            logging.info(f"Extracting file: '{file_info['csv']}' from '{file_info['zip']}' to 'downloads' folder.")
            with zipfile.ZipFile(os.path.join(DOWNLOADS_PATH, file_info['zip']), 'r') as zip_file:
                zip_file.extract(file_info['csv'], DOWNLOADS_PATH)

            extracted_file_path = os.path.join(DOWNLOADS_PATH, file_info["csv"])
            if not os.path.exists(extracted_file_path):
                logging.warning(f"File '{file_info['csv']}' was not found after extraction.")
        
        except zipfile.BadZipFile:
            logging.error(f"Bad ZIP file: {file_info['zip']}")
        except KeyError:
            logging.error(f"File '{file_info['csv']}' not found in ZIP: {file_info['zip']}")
        except Exception as e:
            logging.error(f"An error occurred while extracting '{file_info['csv']}': {e}")


def delete_zip_files(file_mappings):
    for file_info in file_mappings:
        try:
            os.remove(os.path.join(DOWNLOADS_PATH, file_info['zip']))
            logging.info(f"file: '{file_info['zip']}' deleted from 'downloads' folder.")

        except FileNotFoundError:
            logging.warning(f"File '{file_info['zip']}' was not found. It may have been deleted already.")


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

    validate_uris(download_uris)
    file_mappings = prepare_files_list(download_uris)
    download_files(download_uris, file_mappings)
    extract_zip_file(file_mappings)
    delete_zip_files(file_mappings)


if __name__ == "__main__":
    main()
