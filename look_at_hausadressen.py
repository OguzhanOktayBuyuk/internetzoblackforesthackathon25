"""
This script counts the number of addresses per Street and Community in the Hausadressen data from the Hackathon.
It outputs a csv file with the number of unique rows per community and street.
"""
import os
import pandas as pd

if __name__ == "__main__":
    # export folder
    export_folder = "data/results/"

    # create the export folder if it doesn't exist
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    # Path to the CSV file
    path_data = \
        "Hackathon/Daten Hackaton (ALKIS,Nexiga,PV,HK)/Datenquellen/Hauskoordinaten/adressen_bw.txt"

    # Import the CSV file
    hausadressen_gmd_str = pd.read_csv(
        path_data, on_bad_lines='skip', usecols=['gmd', 'str'],
        sep=';', decimal=',')

    # Show the column names
    print(hausadressen_gmd_str.columns)

    # count the number of unique rows per gmd and str
    print("Count of unique rows per gmd and str:")
    n_gmd_str = \
        hausadressen_gmd_str.groupby(['gmd', 'str']).size().reset_index(name='count')

    # export to csv
    n_gmd_str.to_csv(export_folder + "n_gmd_str.csv", index=False)
