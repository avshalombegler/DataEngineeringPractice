import os
import requests
import zipfile 

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_PATH = os.path.join(BASE_PATH, "downloads")
CSV = ".csv"

zip_files_names = []
csv_files_names = []


download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

def get_zip_files_names():
    for uri in download_uris:
        zip_files_names.append(uri.split('/')[-1])


def download_files():
    if not os.path.exists(DOWNLOADS_PATH):
        os.mkdir(DOWNLOADS_PATH)
        print("'downloads' folder created.")

    for (uri, zip_file_name) in zip(download_uris, zip_files_names):
        response = requests.get(uri)
        with open(os.path.join(DOWNLOADS_PATH, zip_file_name), "wb") as uri:
            uri.write(response.content)
            print(f"file: '{zip_file_name}' downloaded to 'downloads' folder.")


def get_csv_files_names():
    for file in zip_files_names:
        csv_files_names.append(file.split('.')[0] + CSV)


def extract_zip_file():
    try:
        for (zip_file, csv_file) in zip(zip_files_names, csv_files_names):
            print(f"Extracting file: '{csv_file}' from '{zip_file}' to 'downloads' folder.")
            with zipfile.ZipFile(os.path.join(DOWNLOADS_PATH, zip_file), 'r') as zip_file:
                zip_file.extract(csv_file, DOWNLOADS_PATH)

    except zipfile.BadZipFile:
        print(f"Error occured when tried to unzip file: '{zip_file}'")

    except FileNotFoundError:
        print(f"File Not Found Error when tried to unzip file: '{zip_file}'")

def delete_zip_files():
    try:
        for zip_file in zip_files_names:
            os.remove(os.path.join(DOWNLOADS_PATH, zip_file))
            print(f"file: '{zip_file}' deleted from 'downloads' folder.")

    except FileNotFoundError:
        print(f"File Not Found Error when tried to unzip file: '{zip_file}'")


def main():

    get_zip_files_names()
    download_files()
    get_csv_files_names()
    extract_zip_file()
    delete_zip_files()


if __name__ == "__main__":
    main()
