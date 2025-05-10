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

    # show the categories for Eigentum
    print("Categories for Eigentum:")
    print(einspeiser_data['Eigentum'].unique())
    print("\n")

    # check if ID is unique
    print("Check if ID is unique:")
    print(einspeiser_data['ID'].is_unique)
    print("\n")

    # check if B Position is unique
    print("Check if B Position is unique:")
    print(einspeiser_data['B Position'].is_unique)
    print("\n")

    # count Gewinnung
    print("Count of Gewinnung:")
    print(einspeiser_data['Gewinnung'].value_counts())
    print("\n")

    # count the number of solar panels per Straﬂe
    print("Count of solar panels per Straﬂe:")
    print(einspeiser_data.groupby('Straﬂe')['ID'].count())
    print("\n")

    # filter on Eigentum == "(fremd) fremd", count the number of solar panels per Straﬂe
    print("Count of solar panels per Straﬂe for Eigentum == '(fremd) fremd':")
    solar_panels_per_street = \
        einspeiser_data[einspeiser_data['Eigentum'] == '(fremd) fremd'].groupby(['Straﬂe', 'Gemeinde'])['ID'].count()
    print(solar_panels_per_street)

    # filter on Eigentum == "(fremd) fremd", add up the amount of '(Peak-)Leistung [kW]'
    print("Sum of '(Peak-)Leistung [kW]' for Eigentum == '(fremd) fremd':")
    leistung_per_street = \
        einspeiser_data[einspeiser_data['Eigentum'] == '(fremd) fremd'].groupby(['Straﬂe', 'Gemeinde'])['(Peak-)Leistung [kW]'].sum()
    print(leistung_per_street)
    print("\n")

    # leistung per Gemeinde
    print("Sum of '(Peak-)Leistung [kW]' per Gemeinde:")
    leistung_per_gemeinde = einspeiser_data.groupby(['Gemeinde'])['(Peak-)Leistung [kW]'].sum()
    print(leistung_per_gemeinde)

    # export solar_panels_per_street to csv
    solar_panels_per_street.to_csv(f"{export_folder}/solar_panels_per_street.csv", sep=';', encoding=encoding)

    # export leistung_per_street to csv
    leistung_per_street.to_csv(f"{export_folder}/leistung_per_street.csv", sep=';', encoding=encoding, decimal=',')

    # export leistung_per_gemeinde to csv
    leistung_per_gemeinde.to_csv(f"{export_folder}/leistung_per_community.csv", sep=';', encoding=encoding, decimal=',')





