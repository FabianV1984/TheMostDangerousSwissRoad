#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import networkx as nx
import osmnx as ox
from pyproj import Transformer
import folium
import numpy as np


# In[2]:


# get accident data
df_acc = pd.read_csv("RoadTrafficAccidentLocations.csv")


# In[3]:


df_acc.head()


# In[4]:


# create geodataframe of accidents
gdf_acc = gpd.GeoDataFrame(
    df_acc,
    geometry=gpd.points_from_xy(
        df_acc["AccidentLocation_CHLV95_E"], df_acc["AccidentLocation_CHLV95_N"]
    ),
    crs="EPSG:2056",
).to_crs("epsg:4326")


# In[5]:


gdf_acc.head(5)


# In[7]:


# get OSM data for investigated location
G = ox.graph_from_place("Luzern, Switzerland", network_type="drive")
G_proj = ox.project_graph(G)
gdf_nodes, gdf_edges = ox.utils_graph.graph_to_gdfs(G_proj)


# In[8]:


# project graph and points
gdf_loc_p = gdf_loc["geometry"].to_crs(G_proj.graph["crs"])

ne, d = ox.nearest_edges(
    G_proj, X=gdf_loc_p.x.values, Y=gdf_loc_p.y.values, return_dist=True
)


# In[33]:


gdf_loc_p


# In[32]:


get_ipython().run_line_magic('time', 'ne1 = ox.nearest_edges(G_proj, X=gdf_loc_p.x.values, Y=gdf_loc_p.y.values, return_dist=True)')


# In[9]:


# reindex points based on results from nearest_edges
gdf_loc = (
    gdf_loc.set_index(pd.MultiIndex.from_tuples(ne, names=["u", "v", "key"]))
    .assign(distance=d)
    .sort_index()
)


# In[36]:


gdf_loc.head(10)


# In[ ]:





# In[ ]:


get_ipython().run_line_magic('time', 'ne1')


# In[18]:


# join geometry from edges back to points
gdf_bad_roads = gdf_edges.join(gdf_loc, rsuffix="_loc", how="inner")
# aggregate so have number of accidents on each edge
bad_roads_2 = gdf_bad_roads.groupby(["u", "v", "key"]).agg({"geometry":"first", "AccidentUID":"size"}).set_crs(gdf_edges.crs).explore(color="blue")


# In[21]:


bad_roads_2


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




