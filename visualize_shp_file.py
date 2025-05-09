import geopandas as gpd
import matplotlib.pyplot as plt

def plot_shapefile_w_background(
    shapefile_path: str,
    background_path: str = "data/zipcodes_baden/plz_baden.shp",
    title: str = "Shapefile Plot"):
    """
    Plots a shapefile using geopandas and matplotlib.
    Zipcodes of Baden as background.
    
    Parameters:
        shapefile_path (str): Path to the shapefile to be plotted.
    """
    # Read the shapefile
    map_data = gpd.read_file(shapefile_path)
    background = gpd.read_file(path_background)

    # change crs of zipcodes to match cable
    background = background.to_crs(map_data.crs)

    # Create a figure and axis
    plt.figure(figsize=(10, 10))

    # Plot the shapefile
    background.plot(ax=plt.gca(), color='lightblue', alpha=0.5)
    map_data.plot(ax=plt.gca())

    # Add title and display
    plt.show()

if __name__ == "__main__":
    path_ms_cable = \
        "Hackathon/Strom ST NS-HA-Kasten BP Position.shp"

    path_background = "data/zipcodes_baden/plz_baden.shp"

    plot_shapefile_w_background(path_ms_cable, path_background)
