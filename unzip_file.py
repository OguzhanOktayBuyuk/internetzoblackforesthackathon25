import os
import sys
import zipfile

def unzip_single_file(zip_path, destination_dir):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(destination_dir)
        print(f"Successfully extracted {zip_path}")
    except Exception as e:
        print(f"Error processing {zip_path}: {str(e)}")

if __name__ == "__main__":
    folder = "Hackathon/Daten Hackaton (ALKIS,Nexiga,PV,HK)/Datenquellen/ALKIS"

    # get all zip files in the folder
    zip_files = [f for f in os.listdir(folder) if f.endswith('.zip')]

    # print the zip files
    print("Found zip files:")
    for zip_file in zip_files:
        print(zip_file)

    # unzip the ALKIS data
    for zip_file in zip_files:
        zip_path = os.path.join(folder, zip_file)
        destination_dir = os.path.join(folder, os.path.splitext(zip_file)[0])
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        unzip_single_file(zip_path, destination_dir)

