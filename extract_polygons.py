import os
import argparse
import osmnx as ox
from osmnx.features import features_from_bbox
import geopandas as gpd
import matplotlib.pyplot as plt

def extract_by_place(place_name, output_path=None, plot=False):
    print(f"Extracting polygon for: {place_name}")
    gdf = ox.geocode_to_gdf(place_name)

    if plot:
        gdf.plot()
        plt.title(place_name)
        plt.axis("equal")
        plt.show()

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        gdf.to_file(output_path, driver="GeoJSON")
        print(f"Saved to {output_path}")
    else:
        print("No output file specified, skipping save.")


def extract_by_bbox(north, south, east, west, output_path=None, plot=False):
    print(f"Extracting features in bounding box: N={north}, S={south}, E={east}, W={west}")

    # Your API expects (west, south, east, north) = (left, bottom, right, top)
    bbox = (west, south, east, north)

    #tags = {"natural": ["coastline", "beach", "scrub", "wood", "bare_rock"]}
    tags = {"place": ["island"]}

    gdf = features_from_bbox(bbox, tags)

    if gdf.empty:
        print("No features found.")
    else:
        if plot:
            gdf.plot()
            plt.title("Bounding Box Extraction")
            plt.axis("equal")
            plt.show()

        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            gdf.to_file(output_path, driver="GeoJSON")
            print(f"Saved to {output_path}")
        else:
            print("No output file specified, skipping save.")




def main():
    north = 45.805
    south = 45.795
    east  = -80.240
    west  = -80.255
    bbox = (north, south, east, west)

    #tags = {"place": "island"}
    tags  = {"natural": "coastline"}
    tags = {"place": "island", "natural": ["coastline", "beach", "scrub", "wood", "bare_rock"]}
    extract_by_bbox(*bbox, output_path=None, plot=True)

if __name__ == "__main__":
    main()