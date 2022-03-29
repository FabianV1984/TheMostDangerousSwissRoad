#!/usr/bin/env python
# coding: utf-8

# # Geodatenhandling 1
# 
# **Inhalt:** Etwas mehr als nur erste Schritte mit Geopandas
# 
# **Nötige Skills**
# - Basic pandas skills
# - Funktionen und pandas
# - Erste Schritte mit Geopandas
# 
# **Lernziele**
# - Koordinatensysteme kennenlernen
# - Koordinaten transformieren
# - Spatial Joins
# - Choropleth maps

# ## Das Beispiel
# 
# Coop-Läden in der Schweiz.
# - Liste "gescrapt" von hier: https://www.coop.ch/de/services/standorte-und-oeffnungszeiten.html
# - Siehe File `Coop.ipynb`
# 
# Wir wollen diese Läden auf einer Karte als Punkte darstellen und wollen ausserdem auswerten, in welchen Kantonen es wieviele Läden gibt!

# ## Setup

# In[1]:


import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString


# ## Import

# **Wir verwenden wiederum ein Shapefile der Kantone**

# In[2]:


gdf_kantone = gpd.read_file('dataprojects/Projections/shp/g1k17.shp', encoding='utf-8')


# In[3]:


gdf_kantone.plot()


# **Liste der Coop-Läden**

# In[4]:


df_stores = pd.read_csv('dataprojects/Coop/geschaefte.csv')


# In[5]:


df_stores.head()


# In[6]:


df_stores['typ'].value_counts()


# ## Geometrie

# Wir müssen aus unserer Liste wiederum ein GeoDataFrame erstellen.
# 
# Die Schritte dazu sind:
# - Identifizieren, welche Spalte die geografischen Infos enthält
# - Geometrie-Spalte im Dataframe erstellen
# - Aus Dataframe ein GeoDataFrame machen

# **Spalte identifizieren**

# In[7]:


df_stores.columns


# Mehr Infos zum geodetic system: https://gps-coordinates.org/

# **Geometrie erstellen**

# In[8]:


df_stores['Punkt'] = df_stores.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)


# In[9]:


df_stores.head(2)


# **Geodataframe kreieren**

# In[10]:


gdf_stores = gpd.GeoDataFrame(df_stores, geometry='Punkt')


# In[11]:


gdf_stores.head(2)


# Hat es funktioniert?

# In[12]:


gdf_stores.plot()


# ## Koordinaten transformieren

# Machen wir nun dasselbe wie im vorherigen Notebook: Plotten wir die Coop-Standorte auf die Schweizer Karte!

# In[13]:


ax = gdf_kantone.plot(figsize=(14,10), color='lightgrey', edgecolor='white')
gdf_stores.plot(markersize=3, ax=ax)


# Das Problem ist: die beiden Geodataframes verwenden verschiedene Koordinatensysteme!
# 
# Das Koordinatensystem in Geodataframes ist in der Property `crs` gespeichert.

# **Kantone: Schweizer Koordinatensystem**
# siehe: https://de.wikipedia.org/wiki/Schweizer_Landeskoordinaten

# In[14]:


gdf_kantone.crs


# **Geschäfte: Haben noch keines!**

# In[15]:


gdf_stores.crs


# Allerdings wissen wir, dass die Koordinaten im world geodetic system kodiert sind. Um dies Geopandas mitzuteilen, müssen wir das Geodataframe mit einem bestimmten Code initiatilisieren:

# In[16]:


gdf_stores.crs = {'init': 'epsg:4326'}


# In[17]:


gdf_stores.crs


# **EPSG-Codes**
# 
# EPSG steht für European Petroleum Survey Group:
# - https://epsg.io/
# 
# Jedes Koordinatensystem hat eine Nummer
# - https://de.wikipedia.org/wiki/European_Petroleum_Survey_Group_Geodesy#EPSG-Codes
# 
# Ein paar gängige Nummern

# | Code | Description |
# |------|---------------------------|
# | 4326 | #world geodetic system |
# | 3857 | #mercator |
# | 2163 | #nice aea projection for the USA |
# | 5071 | #another good one for the USA |
# | 3395 | #mercator (anotherone) |
# | 21781 | #swiss coordinate system |

# Wir wollen das Schweizer Koordinatensystem verwenden. Um die Koordinaten zu transformieren, verwenden wir `to_crs()`:

# In[18]:


gdf_stores.to_crs(epsg=21781)


# Alternativ können wir statt die EPSG-Nummer auch einfach das crs des Kantons-GDF spezifizieren:

# In[19]:


gdf_stores = gdf_stores.to_crs(gdf_kantone.crs)


# Jetzt sind beide Geodataframes im selben Koordinatensystem kodiert und wir können sie auf einer Karte plotten

# In[20]:


ax = gdf_kantone.plot(figsize=(14,10), color='lightgrey', edgecolor='white')
gdf_stores.plot(markersize=3, ax=ax)


# **Zusatzaufgabe:** Plotten Sie die verschiedenen Geschäftstypen je in eigenen Farben!

# In[21]:


colors = {
    'retail': 'blue',
    'pronto': 'green',
    'id': 'orange',
    'restaurant': 'red',
    'impo': 'darkblue',
    'vitality': 'darkgreen',
    'bh': 'black',
    'christ': 'black',
    'city': 'black',
    'livique': 'black',
    'togo': 'black',
    'lumimart': 'black',
    'takeit': 'black',
    'marche': 'black',
    'hotel': 'black',
    'capuccini': 'black',
    'burger': 'black',
    'toptip': 'black',
    'cindy': 'black',
    'sapori': 'black',
    'zopf': 'black',
    'karma': 'black',
    'halba': 'black',
    'perpiedi': 'black'
}


# In[22]:


colorlist = gdf_stores['typ'].apply(lambda typ: colors[typ])


# In[23]:


colorlist.value_counts(dropna=False)


# In[24]:


ax = gdf_kantone.plot(figsize=(14,10), color='lightgrey', edgecolor='white')
gdf_stores.plot(markersize=3, ax=ax, color=colorlist, alpha=0.6)


# In[ ]:





# ## Geo-Selektion
# 
# Was könnten wir nun mit diesen beiden Datensets anfangen, die im selben System kodiert sind (ausser sie zu plotten)?
# 
# Zum Beispiel:
# - Einzelne Geschäfte selektieren (je nach Kanton)
# - Gschäfte pro Kanton zählen

# ### spatial joins

# Ähnlich wie `merge()` in Pandas bietet auch Geopandas eine Funktion an, um zwei Datensets zu kombinieren: `sjoin()`

# In[25]:


gdf_merged = gpd.sjoin(gdf_stores, gdf_kantone, how='left', predicate='within')


# Wir wählen hier zu jeder Zeile aus dem ersten GDF (gdf_stores, also die Geschäfte) die passende Zeile aus dem anderen GDF (gdf_kantone, also den passenden Kanton) aus.
# 
# `how=` gibt wie in pandas an, wie wir matchen wollen:
# - "left"
# - "right"
# - "inner"
# - "outer"
# 
# `predicate=` (bzw. in einer früheren Version: `op=()`) gibt die geometrische matching-methode an:
# - "contains" (linke geometrie enthält rechte geometrie)
# - "within" (linke geometrie ist innnerhalb rechter geometrie)
# - "intersects" (linke geometrie überschneidet sich mit rechter geometrie)

# In unserem Fall haben wir also gesagt:
# - suche zu jedem store-punkt das passende kantons-polygon
# - wobei der punkt innerhalb des polygons liegen muss
# 
# Nun haben wir ein zusammengeführtes, ziemlich breites geodataframe:

# In[26]:


gdf_merged.columns


# Und das Gute ist: zu jeder Coop-Filiale ist nun die Information enthalten, in welchem Kanton sie liegt.

# In[27]:


gdf_merged['KTNAME']


# Das ermöglicht uns zB, nur Stores aus einem einzelnen Kanton zu bearbeiten:

# In[28]:


ax = gdf_kantone[gdf_kantone['KTNAME'] == 'Zürich'].plot(color='lightgrey', edgecolor='white', figsize=(6,8))
gdf_merged[gdf_merged['KTNAME'] == 'Zürich'].plot(markersize=3, alpha=0.6, ax=ax)


# ## Geo-Information darstellen

# Wie viele Läden sind in welchem Kanton? Diese Frage können wir nun beantworten:

# In[29]:


gdf_merged['KTNAME'].value_counts()


# Um diese Information wiederum geografisch darzustellen, können wir sie zurück in unser Kantone-GDF mergen.

# **Vorbereitung:**

# In[30]:


df_anzahl = gdf_merged['KTNAME'].value_counts().to_frame()


# In[31]:


df_anzahl = df_anzahl.rename(columns={'KTNAME': 'Anzahl'})


# In[32]:


df_anzahl.head(5)


# **Merge:**

# In[33]:


gdf_kantone_anzahl = gdf_kantone.merge(df_anzahl, how='inner', left_on='KTNAME', right_index=True)


# In[34]:


gdf_kantone_anzahl.head(2)


# **Plot:**
# 
# Dokumentation zum Plotten in Geopandas, Siehe auch:
# - http://geopandas.org/mapping.html
# - https://github.com/MAZ-CAS-DDJ/kurs_21_22/blob/master/00%20weitere%C2%A0Dokumente/hilfsmaterial/geopandas.md
# 
# und:
# 
# https://blog.datawrapper.de/choroplethmaps/
# 
# Wir können Geopandas in der `plot()`-Funktion angeben, wie die Farbcodierung erstellt werden soll.
# 
# - `column=` - welche Spalte verwendet werden soll: in unserem Fall, "Anzahl"
# - `cmap=` - welche Colormap werwendet werden soll: https://matplotlib.org/examples/color/colormaps_reference.html
# - `scheme=` - kann "equal_interval" oder "quantiles" sein. Standardzahl der Schritte ist 5.

# In[35]:


ax = gdf_kantone_anzahl.plot(column='Anzahl', cmap='Blues', scheme='quantiles', edgecolor='white', legend=True, figsize=(12,12))
ax.set_title('Anzahl Coop-Filialen pro Kanton')


# In[ ]:




