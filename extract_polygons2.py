import os
import osmnx as ox
from osmnx.features import features_from_bbox
import geopandas as gpd
import matplotlib.pyplot as plt
import pickle
import numpy as np

def extract_island_polygons(north, south, east, west, output_path=None, plot=False):
    print(f"Extracting island features in: N={north}, S={south}, E={east}, W={west}")

    # Correct order: north > south, east > west
    if north < south or east < west:
        raise ValueError("Bounding box coordinates are invalid. Check north/south/east/west.")

    # Define OSM tags for islands and natural features
    tags = {
        "place": "island",
        "natural": ["coastline", "beach", "scrub", "wood", "bare_rock"]
    }

    # Extract data
    bbox = (west, south, east, north)  # OSMnx expects (west, south, east, north)

    gdf = features_from_bbox(bbox, tags=tags)

    if gdf.empty:
        print("No features found.")
        return

    # Project to UTM zone 17N (covers Georgian Bay region)
    gdf_proj = gdf.to_crs(epsg=32617)

    if plot:
        gdf_proj.plot()
        plt.title("Projected Island Polygons (UTM Zone 17N)")
        plt.axis("equal")
        plt.show()

    # Save or return
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        gdf_proj.to_file(output_path, driver="GeoJSON")
        print(f"Saved projected polygons to {output_path}")
    else:
        print("No output file specified. Returning projected GeoDataFrame.")
        return gdf_proj



def save_island_polygons_to_pickle(bbox, output_path, plot=False, epsg=32617):
    """
    Download island polygons from OSM and save them to a pickle file.

    Parameters:
        bbox (tuple): Bounding box in (west, south, east, north)
        output_path (str): Path to save the .pkl file
        plot (bool): Whether to plot the polygons
        epsg (int): EPSG code for projection (default UTM zone 17N)
    """
    tags = {
        "place": "island",
        "natural": ["coastline", "scrub", "wood", "bare_rock"]
    }

    print(f"Downloading features from bbox: {bbox}")
    gdf = features_from_bbox(bbox, tags=tags)

    if gdf.empty:
        print("No features found.")
        return

    gdf_proj = gdf.to_crs(epsg=epsg)

    if plot:
        gdf_proj.plot()
        plt.title("Projected Island Polygons")
        plt.axis("equal")
        plt.show()

    with open(output_path, "wb") as f:
        pickle.dump(gdf_proj, f)

    print(f"Saved {len(gdf_proj)} island polygons to: {output_path}")


def save_polygon_coords_only(gdf, output_path):
    all_coords = []

    for geom in gdf.geometry:
        if geom.geom_type == 'Polygon':
            coords = np.array(geom.exterior.coords)
            all_coords.append(coords)
        elif geom.geom_type == 'MultiPolygon':
            for poly in geom.geoms:
                coords = np.array(poly.exterior.coords)
                all_coords.append(coords)

    with open(output_path, "wb") as f:
        pickle.dump(all_coords, f)

    print(f"Saved {len(all_coords)} polygon coordinate arrays to: {output_path}")

def main():
    # Bounding box around Starr Island (rough estimate – you can refine this)
    lat_center = 25.505901 
    lon_center = 29.421257
    
    #lat_center = 45.696039
    #lon_center = -80.618887
    # Bounding box with ±0.002 degrees (~220m N/S and ~150m E/W)
    north = lat_center + 2
    south = lat_center - 2
    east  = lon_center + 2
    west  = lon_center - 2

    # Output GeoJSON file (optional)
    output_path = "output/georgian_bay_islands_projected.geojson"

    # Call the extraction function
    gdf = extract_island_polygons(north, south, east, west, output_path = None, plot=True)

    # Example usage of save_island_polygons_to_pickle
    bbox = (west, south, east, north)  # OSMnx expects (west, south, east, north)
    pickle_output_path = "output/georgian_bay_islands.pkl"
    save_island_polygons_to_pickle(bbox, pickle_output_path, plot=True, epsg=32617)
    save_polygon_coords_only(gdf, "output/georgian_bay_islands_coords.pkl")

if __name__ == "__main__":
    main()