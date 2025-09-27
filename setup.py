# setup.py

from setuptools import setup, find_packages

setup(
    name='osm_land_polygons',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # These are the necessary non-standard libraries
        'osmnx', 
        'geopandas',
        'matplotlib', 
        'numpy',
    ],
)