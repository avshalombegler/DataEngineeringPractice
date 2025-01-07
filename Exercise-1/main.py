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


def download_files():
    if not os.path.exists(DOWNLOADS_PATH):
        os.mkdir(DOWNLOADS_PATH)
        print("'downloads' folder created.")

    for uri in download_uris:
        response = requests.get(uri)
        zip_files_names.append(uri.split('/')[-1])
        with open(os.path.join(DOWNLOADS_PATH, zip_files_names[-1]), "wb") as uri:
            uri.write(response.content)
            print(f"file: {zip_files_names[-1]} downloaded to 'downloads' folder.")


def get_files_names():
    for file in zip_files_names:
        csv_files_names.append(file.split('.')[0] + CSV)


def extract_zip_file():
    try:
        for (zip_file, csv_file) in zip(zip_files_names, csv_files_names):
            with zipfile.ZipFile(os.path.join(DOWNLOADS_PATH, zip_file), 'r') as zip_file:
                zip_file.extract(csv_file, DOWNLOADS_PATH)
                print(f"file: {csv_file} extracted to 'downloads' folder.")

    except zipfile.BadZipFile:
        print(f"Error occured when tried to unzip file: {zip_file}")

    except FileNotFoundError:
        print(f"File Not Found Error when tried to unzip file: {zip_file}")

def delete_zip_files():
    try:
        for zip_file in zip_files_names:
            os.remove(os.path.join(DOWNLOADS_PATH, zip_file))

    except FileNotFoundError:
        print(f"File Not Found Error when tried to unzip file: {zip_file}")


def main():

    download_files()
    get_files_names()
    extract_zip_file()
    delete_zip_files()


if __name__ == "__main__":
    main()
