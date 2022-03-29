#!/usr/bin/env python
# coding: utf-8

# # Geodatenhandling 2
# 
# **Inhalt:** Geopandas für Fortgeschrittene
# 
# **Nötige Skills**
# - Basic pandas skills
# - Funktionen und pandas
# - Erste Schritte mit Geopandas
# - Geodatenhandling 1
# 
# **Lernziele**
# - Punkte, Linien, Polygone revisited
# - Eigenschaften von geometrischen Shapes
# - Shapes modifizieren und kombinieren
# - Geodaten modifizieren und selektieren

# ## Das Beispiel
# 
# Geschäfte in Chicago.
# 
# Wir checken: In welchen Stadtteilen gibt es keine Lebensmittelläden, wo sind die "Food deserts"
# 
# - `Boundaries - Census Tracts - 2010.zip`, census tracts in Chicago from [here](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Census-Tracts-2010/5jrd-6zik)
# - `Grocery_Stores_-_2013.csv`, grocery stores in Chicago from [here](https://data.cityofchicago.org/Community-Economic-Development/Grocery-Stores-2013/53t8-wyrc)
# 
# **Credits to:**
# - http://www.jonathansoma.com/lede/foundations-2017/

# ## Setup

# In[1]:


import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon


# In[ ]:





# ## Geometries
# 
# Zum Aufwärmen, nochmals ein paar Shapes from scratch

# ### Point (again)

# In[2]:


punkt1 = Point(5, 5)


# In[3]:


punkt1


# ### Line (again)

# In[4]:


linie1 = LineString([Point(20, 0), Point(0, 20)])


# In[5]:


linie1


# In[6]:


linie2 = LineString([Point(15, 0), Point(0, 15)])


# In[7]:


linie3 = LineString([Point(25, 0), Point(0, 25)])


# In[ ]:





# ### Polygon (again)

# In[8]:


polygon1 = Polygon([[0, 0], [10, 0], [10, 10], [0, 10]])


# In[9]:


polygon1


# **Let's plot it together!**

# In[10]:


df = pd.DataFrame({'geometry': [punkt1, linie1, linie2, linie3, polygon1]})


# In[11]:


gdf = gpd.GeoDataFrame(df, geometry='geometry')


# In[12]:


gdf


# In[13]:


gdf.plot(alpha=0.5, linewidth=2, edgecolor='black', markersize=5)


# ## Shapes vergleichen
# 
# Wir können geometrische Shapes auf verschiedene Weise miteinander "vergleichen".

# * **contains:** has the other object TOTALLY INSIDE  (boundaries can't touch!!!) "a neighborhood CONTAINS restaurants"
# * **intersects:** is OVERLAPPING at ALL, unless it's just boundaries touching
# * **touches:** only the boundaries touch, like a tangent
# * **within:** is TOTALLY INSIDE of the other object "a restaurant is WITHIN a neighborhood"
# * **disjoint:** no touching!!! no intersecting!!!!
# * **crosses:** goes through but isn't inside - "a river crossing through a city"
# 
# Referenz und weitere Vergleiche: http://geopandas.org/reference.html)

# Das funktioniert ganz einfach:

# In[14]:


polygon1.contains(punkt1)


# In[15]:


punkt1.contains(polygon1)


# **Quizfragen:**

# In[16]:


#Liegt der Punkt 1 innerhalb von Polygon 1?
punkt1.within(polygon1)


# In[17]:


#Berührt die Linie 1 das Polygon 1?
linie1.touches(polygon1)


# In[18]:


#Überschneidet sich die Linie 3 mit dem Polygon 1?
linie3.intersects(polygon1)


# In[19]:


#Überschneidet sich die Linie 2 mit dem Polygon 1?
linie2.intersects(polygon1)


# In[20]:


#Ist das Polygon 1 völlig losgelöst von der Linie 3?
polygon1.disjoint(linie3)


# ## Import
# 
# Und nun zu unserem Beispiel:

# **Ein Stadtplan von Chicago mit den Quartieren (census tracts)**

# In[21]:


tracts = gpd.read_file("dataprojects/Food Deserts/Boundaries - Census Tracts - 2010/geo_export_085dcd7b-113c-4a6d-8d43-5926de1dcc5b.shp")


# In[22]:


tracts.head(2)


# In[23]:


tracts.plot()


# **Eine Liste aller Lebensmittelläden**

# In[24]:


df = pd.read_csv("dataprojects/Food Deserts/Grocery_Stores_-_2013.csv")


# In[25]:


df.head(2)


# Um von Pandas zu Geopandas zu gelangen:
# - Geometrie erstellen
# - Geodataframe erstellen
# - Koordinatensystem intialisieren

# In[26]:


points = df.apply(lambda row: Point(row['LONGITUDE'], row['LATITUDE']), axis=1)


# In[27]:


grocery_stores = gpd.GeoDataFrame(df, geometry=points)


# In[28]:


grocery_stores.crs = {'init': 'epsg:4326'}


# In[29]:


grocery_stores.plot()


# **Wir plotten mal alles zusammen**

# In[30]:


ax = tracts.plot(figsize=(15,15), color='lightgrey', linewidth=0.25, edgecolor='white')
grocery_stores.plot(ax=ax, color='red', markersize=8, alpha = 0.8)


# ## Analyse
# 
# Uns interessiert: Wo sind die Gebiete, in denen es in einem bestimmten Umkreis von Metern keine Lebensmittelläden gibt?
# 
# Um das zu beantworten, müssen wir zuerst in ein brauchbares Koordinatensystem wechseln, das auf Metern basiert.

# ### Projektion ändern
# 
# Wir entscheiden uns für eine Variante der Mercator-Projektion.
# Das ist praktisch, weil:
# - "Die wichtigste Eigenschaft der Mercator-Projektion ist ihre Winkeltreue. Diese bedeutet auch, dass in kleinen Bereichen der Längenmaßstab in allen Richtungen gleich ist." https://de.wikipedia.org/wiki/Mercator-Projektion
# - Die Koordinaten sind nicht in Längen-/Breitengrad, sondern in Metern angegeben (die CH-Koordinaten sind auch eine Variante der Mercator-Projektion)

# In[31]:


grocery_stores = grocery_stores.to_crs({'proj': 'merc'})
tracts = tracts.to_crs({'proj': 'merc'})


# Andere Projektionen wären:
# - 'tmerc': transverse mercator
# - 'aea': albers equal area

# **Wir haben nun ein neues Koordinatensystem**

# In[32]:


ax = tracts.plot(figsize=(15,15), color='lightgrey', linewidth=0.25, edgecolor='white')
grocery_stores.plot(ax=ax, color='red', markersize=8, alpha = 0.8)


# ### Buffer erstellen
# 
# Wie sieht die Karte aus, wenn wir um jedes Lebensmittelgeschäft einen Kreis von 500 Metern ziehen?

# In[33]:


ax = tracts.plot(figsize=(15,15), color='lightgrey', linewidth=0.25, edgecolor='white')
grocery_stores.buffer(500).plot(ax=ax, color='red', markersize=8, alpha=0.4)


# ### Union
# 
# Nächster Schritt: Wir fügen alle Punkte zu einer Fläche zusammen

# In[34]:


near_area = grocery_stores.buffer(500).unary_union


# Jetzt können wir testen, ob die einzelnen Quartiere diese Fläche berühren

# In[35]:


tracts.disjoint(near_area)


# In[36]:


tracts[tracts.disjoint(near_area)].plot()


# ### Plot
# 
# Wir plotten dieselbe Karte wie vorher - und zusätzlich noch jene Tracts, welche die Punktefläche nicht berühren

# In[37]:


#Bisherige Karte
ax = tracts.plot(figsize=(15,15), color='lightgrey', linewidth=0.25, edgecolor='white')
grocery_stores.buffer(500).plot(ax=ax, color='red', markersize=8, alpha=0.4)

#Neu: Desert-Tracts
tracts[tracts.disjoint(near_area)].plot(ax=ax, color='darkblue', alpha=0.4)

ax.set_title('City tracts that have no grocery store within 500m distance')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




