

import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt


def convert_shapefile_to_csv(shapefile_path: str, output_csv_path: str):
    """
    Converts a shapefile to a CSV file.
    
    Parameters:
        shapefile_path (str): Path to the shapefile to be converted.
        output_csv_path (str): Path where the CSV file will be saved.
    """
    # Read the shapefile
    map_data = gpd.read_file(shapefile_path)

    # Save the dataframe to a csv file
    map_data.to_csv(output_csv_path, index=False)

if __name__ == "__main__":
    # # Path to the shapefile
    # path_data = \
    #     "Hackathon/Daten Hackaton (ALKIS,Nexiga,PV,HK)/Datenquellen/Nexiga Daten/nexiga_all.shp"

    # # Path where the CSV file will be saved
    # output_csv_path = "nexiga_all.csv"

    # # Convert the shapefile to CSV
    # convert_shapefile_to_csv(path_data, output_csv_path)

    # import the csv file
    path_data = "data/inputs/nexiga_all.csv"

    # import the csv file
    nexiga_data = pd.read_csv(path_data)

    # show the column names
    print(nexiga_data.columns)

    # does every row have a lcewb?
    print("Does every row have a lcewb?")
    print(nexiga_data['lcewb'].notna().all())
    print("\n")

    # how many rows are there?
    print(f"Number of rows: {len(nexiga_data)}")

    # how many KGS22 Wohnquartierskennziffer are there?
    print(f"Number of KGS22 Wohnquartierskennziffer: {len(nexiga_data['kgs22'].unique())}")

    # print all kgs8 names
    print(f"Unique KGS8 names: {nexiga_data['kgs8_name'].unique()}")

    # how many KGS22 Wohnquartierskennziffer are there for community Freiburg?
    print(f"Number of KGS22 Wohnquartierskennziffer for community Freiburg: {len(nexiga_data[nexiga_data['kgs8_name'] == 'Freiburg im Breisgau, Stadt']['kgs22'].unique())}")

    # how many rows are there for each kgs22?
    print(nexiga_data.groupby('kgs22').size())




