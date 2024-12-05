#config
from pathlib import Path
from scripts.path import PATH
debug = False

# System
import csv
import sys
import os
import watermark
import pickle
import itertools
import random
import zipfile
from collections import defaultdict
import pprint
pp = pprint.PrettyPrinter(indent=4)
from tqdm.notebook import tqdm
import warnings
import shutil
import time
from tqdm import tqdm

# Math/Data
import math
import numpy as np
import pandas as pd

# Network
import igraph as ig
import networkx as nx

# Plotting
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib
from matplotlib.collections import PatchCollection
from matplotlib.ticker import MaxNLocator

print("PATH:", PATH)
# Geo
import osmnx as ox
ox.settings.log_file = True
ox.settings.requests_timeout = 300
ox.settings.logs_folder = PATH["logs"]
import fiona
import shapely
from osgeo import gdal, osr
from haversine import haversine, haversine_vector
import pyproj
from shapely.geometry import Point, MultiPoint, LineString, Polygon, MultiLineString, MultiPolygon
import shapely.ops as ops
import geopandas as gpd
import geojson



     
# dict of placeid:placeinfo
# If a city has a proper shapefile through nominatim
# In case no (False), manual download of shapefile is necessary, see below

cities = {}
current_dir = os.getcwd()
print("Current working directory:", current_dir)
with open(PATH["parameters"] / 'cities.csv', mode='r', encoding='utf-8') as f:
    csvreader = csv.DictReader(f, delimiter=';')
    for row in csvreader:
        cities[row['placeid']] = {}
        for field in csvreader.fieldnames[1:]:
            cities[row['placeid']][field] = row[field]    
if debug:
    print("\n\n=== Cities ===")
    pp.pprint(cities)
    print("==============\n\n")

# Create city subfolders  
for placeid, placeinfo in cities.items():
    for subfolder in ["data", "plots", "plots_networks", "results", "exports", "exports_json", "videos"]:
        placepath = PATH[subfolder] / placeid  
        if not placepath.exists():
            placepath.mkdir(parents=True, exist_ok=True)  
            print(f"Successfully created folder {placepath}")


print("Initialization complete.\n")
