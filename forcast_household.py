"""
Veeeeery simple approach to forecast household supply for PV.
"""
import pandas as pd
import numpy as np
import chardet
from region_dict import region_dict, forcast_dict

# forcast_dict = {
#     "Breisach": 0.1,
#     "Freiburg": 0.2,
#     "Kaiserstuhl": 0.3,
#     "RWH": 0.4,
#     "Süd": 0.5
# }

def add_the_badenova_region(df: pd.DataFrame, region_dict: dict) -> pd.DataFrame:
    """
    Add the Badenova region to the dataframe based on the Gemeinde column.
    """
    # create a new column 'region' and set it to NaN
    df['bn_region'] = np.nan

    # iterate over the region_dict
    for region, gemeinde_list in region_dict.items():
        # set the value of the 'region' column to the region name if the Gemeinde is in the list
        df.loc[df['kgs8_name'].isin(gemeinde_list), 'bn_region'] = region

    return df

def forecast_household_supply(df: pd.DataFrame, region_forcast: float) -> pd.DataFrame:
    # compute sum of all values in the column 'predictions'
    total_pred = df['predictions'].sum()

    # add a new col weight which is the ratio of one predictions to the total predictions
    df['weight'] = df['predictions'] / total_pred

    # add a new col forecast which is the ratio of one predictions
    # to the total predictions times the region_forcast
    df['forecast'] = df['weight'] * region_forcast

    return df


if __name__ == "__main__":
    # Path to the CSV file
    path_data = "data/results/rt_solar.csv"

    # Detect the encoding of the CSV file
    # with open(path_data, 'rb') as f:
    #     result = chardet.detect(f.read())
    #     encoding = result['encoding']
    #     print(f"Detected encoding: {encoding}")

    # Import the CSV file
    all_addresses = pd.read_csv(path_data, on_bad_lines='skip', sep=';', decimal=',') #, encoding=encoding)

    # print the share of nans in the column 'Gemeinde'
    print("Share of nans in the column 'Gemeinde':")
    print(all_addresses['kgs8_name'].isna().mean())
    print("\n")

    # Show the column names
    print(all_addresses.columns)

    # print unique values for Gemeinde
    print(all_addresses['kgs8_name'].unique())

    # add the Badenova region to the dataframe
    all_addresses = add_the_badenova_region(
        all_addresses, region_dict
    )

    # print the share of nans in the column 'bn_region'
    print("Share of nans in the column 'bn_region':")
    print(all_addresses['bn_region'].isna().mean())
    print("\n")

    # count the of observators per region
    print("Count of observators per region:")
    print(all_addresses['bn_region'].value_counts())
    print("\n")

    # split the all_addresses by bn_region
    # for each region, compute the forcast
    forcasts = []
    regions = region_dict.keys()

    for region in regions:
        # if region != "nan" or region is not np.nan:
        # print the region
        print(f"Region: {region}")
        print(type(region))

        # get the region data
        region_data = all_addresses[all_addresses['bn_region'] == region]

        # compute the forcast
        region_forcast = forcast_dict[region]["2023"]
        region_data = forecast_household_supply(region_data, region_forcast)

        # print the first 5 rows
        print(f"First 5 rows for {region}:")
        print(region_data.head())
        print("\n")

        # append to forcasts
        forcasts.append(region_data)

    # concat the forcasts
    all_addresses = pd.concat(forcasts)

    # save as csv
    all_addresses.to_csv(
        "data/results/rt_solar_forecast.csv",
        index=False, sep=';',
        decimal=','
    )




