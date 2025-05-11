import geopandas as gpd
import pandas as pd
from shapely import wkt

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('./rt_solar_forecast.csv', delimiter=';')

# Convert the 'geometry' column from WKT to shapely geometries
df['geometry'] = df['geometry'].apply(wkt.loads)

# Create a GeoDataFrame (assuming original CRS is unknown)
gdf = gpd.GeoDataFrame(df, geometry='geometry')

print(gdf.crs)

# Define the current CRS of the data (replace 'EPSG:XXXX' with your current CRS)
# For example, if your data uses UTM (EPSG:32632), set that here
gdf.set_crs('EPSG:25832', allow_override=True, inplace=True)

# Reproject the data to EPSG:4326 (WGS 84 - latitude and longitude)
gdf = gdf.to_crs(3685)

# Save the data as a GeoJSON file
gdf.to_file('formatted_file.geojson', driver='GeoJSONSeq')

