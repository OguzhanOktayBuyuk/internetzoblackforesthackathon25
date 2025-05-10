import geopandas as gpd

def convert_to_csv(path_to_shapefile: str, path_to_output: str):
    """
    Converts a shapefile to csv format.

    Parameters:
        path_to_shapefile (str): Path to the input shapefile.
        path_to_output (str): Path to save the output csv file.
    """
    # Read the shapefile
    gdf = gpd.read_file(path_to_shapefile)

    # Convert to Parquet
    gdf.to_parquet(path_to_output)

if __name__ == "__main__":
    # Example usage
    path_data = "Hackathon/Daten Hackaton (ALKIS,Nexiga,PV,HK)/Datenquellen/Nexiga Daten/nexiga_all.shp"
    path_output = "nexiga_all.parquet"

    convert_to_csv(path_data, path_output)