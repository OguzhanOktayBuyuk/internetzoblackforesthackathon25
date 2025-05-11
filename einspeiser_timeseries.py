"""
This script analyzes the Einspeiser data from the Hackathon.
It outputs the following:
1. The number of solar panels per street for Eigentum == '(fremd) fremd'.
2. The sum of '(Peak-)Leistung [kW]' per street for Eigentum == '(fremd) fremd'.
3. The sum of '(Peak-)Leistung [kW]' per Gemeinde.
"""

import os
import pandas as pd
import chardet

if __name__ == "__main__":
    # export folder
    export_folder = "data/results/"

    # create the export folder if it doesn't exist
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    # Path to the CSV file
    path_data = "Hackathon/Strom-Einspeiser-Export 1.csv"

    # Detect the encoding of the CSV file
    with open(path_data, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']
        print(f"Detected encoding: {encoding}")

    # Import the CSV file
    einspeiser_data = pd.read_csv(path_data, on_bad_lines='skip', encoding=encoding, sep=';', decimal=',')

    # Show the column names
    print(einspeiser_data.columns)

    # Show the first 5 rows
    print(einspeiser_data.head())

    # show Einbaudatum
    print("Einbaudatum:")
    print(einspeiser_data['Einbaudatum'].unique())
    print("\n")

    # convert Einbaudatum to datetime
    einspeiser_data['Einbaudatum'] = \
        pd.to_datetime(einspeiser_data['Einbaudatum'], format='%d.%m.%Y', errors='coerce')

    # create a time series per street (Straﬂe)
    solar_panels_per_street_over_time = \
        einspeiser_data[einspeiser_data['Eigentum'] == '(fremd) fremd'].groupby(
            ['Straﬂe', 'Gemeinde', 'Einbaudatum'])['ID'].count()

    # cumulate over time for Straﬂe and Gemeinde
    solar_panels_per_street_over_time = \
        solar_panels_per_street_over_time.groupby(
            ['Straﬂe', 'Gemeinde']).cumsum().reset_index(name='count')

    # print the first 5 rows
    print(solar_panels_per_street_over_time.head())

    # export to csv
    solar_panels_per_street_over_time.to_csv(
        export_folder + "solar_panels_per_street_over_time.csv",
        index=True, sep=';',
        encoding=encoding, decimal=','
    )
