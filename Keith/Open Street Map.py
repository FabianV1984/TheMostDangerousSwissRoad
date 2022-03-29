#!/usr/bin/env python
# coding: utf-8

# # Open Street Map
# 
# **Inhalt:** Daten aus einer Open Source Quelle ziehen
# 
# **Nötige Skills**
# - Geopandatenhandling
# 
# **Lernziele**
# - Einblick in Funktionsweise von OSM
# - Vor-Aufbereitete OSM-Shapefiles laden
# - Daten herunterladen mit `OSMnx`-Library

# In[1]:


from IPython.display import Image


# In[2]:


import pandas as pd
import geopandas as gpd


# In[3]:


from shapely.geometry import Point, LineString, Polygon


# In[4]:


import networkx as nx
import osmnx as ox


# In[5]:


pd.set_option("display.max_rows", 300)


# ## Über Open Street Map

# «OpenStreetMap is a map of the world, created by people like you and free to use under an open license.»
# 
# https://www.openstreetmap.org
# 
# => Es ist das Google-Street-Map-Äquivalent der Open-Source-Community.

# In[6]:


Image("dataprojects/osm/osm-luzern.png")


# About:
# - https://de.wikipedia.org/wiki/OpenStreetMap
# - https://wiki.openstreetmap.org/wiki/Main_Page

# Man kann auf verschiedenen Wegen Daten aus OSM laden. Hier eine Übersicht: https://learnosm.org/de/osm-data/getting-data/

# ## 1. via API
# 
# Für Softwareentwickler und professionelle Anwender gibt es die OSM API:
# - Overpass API https://wiki.openstreetmap.org/wiki/Overpass_API
# 
# Diese ist recht kompliziert, es gibt spezielles Tool, das einem hilft, den Querystring aufzubauen
# - Overpass Turbo: http://overpass-turbo.eu/
# 
# Wie man diese Tools in Python benutzen kann, liest man zB hier:
# - https://towardsdatascience.com/loading-data-from-openstreetmap-with-python-and-the-overpass-api-513882a27fd0

# Wir schauen uns stattdessen zwei andere Wege an

# ## 2. via Geofabrik

# Hier werden vor-aufbereitete Shapefiles aus OWM zum Download angeboten: http://download.geofabrik.de/

# In[7]:


Image("dataprojects/osm/geofabrik.png")


# Typischerweise werden dabei alle Informationen zu einem Land in ein grosses zip-Archiv gepackt (das Schweiz-File wiegt zB 628 MB!)

# ### Daten laden

# Um die neueste Version zu erhalten: **folgendes Zip-File runterladen**:

# `http://download.geofabrik.de/europe/switzerland-latest-free.shp.zip`

# im ZIP hat es dann einzelne Shapefiles zu verschiedenen Objektkategorien:
# 
# - `gis_osm_buildings_a_free_1.shp`
# - `gis_osm_landuse_a_free_1.shp`
# - `gis_osm_natural_a_free_1.shp`
# - `gis_osm_natural_free_1.shp`
# - `gis_osm_places_a_free_1.shp`
# - `gis_osm_places_free_1.shp`
# - `gis_osm_pofw_a_free_1.shp`
# - `gis_osm_pofw_free_1.shp`
# - `gis_osm_pois_a_free_1.shp`
# - `gis_osm_pois_free_1.shp`
# - `gis_osm_railways_free_1.shp`
# - `gis_osm_roads_free_1.shp`
# - `gis_osm_traffic_a_free_1.shp`
# - `gis_osm_traffic_free_1.shp`
# - `gis_osm_transport_a_free_1.shp`
# - `gis_osm_transport_free_1.shp`
# - `gis_osm_water_a_free_1.shp`
# - `gis_osm_waterways_free_1.shp`

# Hier haben wir das Schweiz-Archiv bereits lokal entpackt.
# 
# *Achtung:*
# - lange Ladezeit...
# - `encoding="utf-8"` beachten

# In[63]:


gdf_osm = gpd.read_file("dataprojects/osm/switzerland-latest-free.shp/gis_osm_buildings_a_free_1.shp", encoding="utf-8")


# Kein Wunder dauert es lange, das Datenfile mit allen Gebäuden der Schweiz hat fast 2,5 Millionen Zeilen.

# In[64]:


gdf_osm.shape


# Der Vorteil an den Geofabrik-Daten: Sie sind sehr schön strukturiert:

# In[65]:


gdf_osm.head()


# ### Datenstruktur

# #### ID
# 
# Jedes Element in diesem Geodataframe hat eine `osm_id`. Diese ID ist der Unique Identifier einer bestimmten Einheit in OSM. Wir treffen sie auch an, wenn wir auf anderem Wege Daten herunterladen oder direkt auf OSM danach suchen.
# 
# Zum Beispiel das KKL Luzern: https://www.openstreetmap.org/relation/1661451

# In[8]:


Image("dataprojects/osm/kkl.png")


# In[67]:


gdf_osm[gdf_osm['osm_id'] == '1661451']


# #### name

# Zu jedem Element, das eine `osm_id` hat, gehört netterweise auch ein `name`.

# #### code 
# 
# Ein vierstelliger Code, der angibt, um was für eine Art von Feature es sich handelt (Strasse, Fluss, Stadt, Point of Interest, Schule, Spital, ...)
# 
# Die ganze Liste der Codes findet sich hier: http://download.geofabrik.de/osm-data-in-gis-formats-free.pdf

# In[68]:


gdf_osm['code'].value_counts()


# #### fclass
# 
# Beschreibt den Code in Worten. Weil wir in diesem Shapefile nur Gebäude geladen haben, lautet er immer `building`.

# In[69]:


gdf_osm['fclass'].value_counts()


# #### geometry
# 
# Die wichtigste Spalte: Enthält die geografischen Infos zu einem Feature, also zu einem Element der Karte. Das kann sein:
# - ein `Point` 
# - ein `Linestring` (z.B. bei einer Strasse)
# - ein `Polygon` (zB bei einem Gebäude)

# Wir können die Geometriespalte nutzen, um zB einen Kartenausschnitt («bbox») für Luzern zu generieren.
# 
# Dazu definieren wir zuerst ein Viereck mit den Eckpunkten: https://tools.retorte.ch/map/?swissgrid=2667889,1209686&zoom=14

# In[70]:


north, south, east, west = 47.06954, 47.03474, 8.2715, 8.33184

Luzern = Polygon([[west, north], [east, north], [east, south], [west, south]])


# In[71]:


Luzern.wkt


# Anschliessend können wir das Geodataframe filtern (das Vergleichskennwort heisst hier `within`)

# In[72]:


gdf_luzern = gdf_osm[gdf_osm.within(Luzern)]


# In[73]:


gdf_luzern.head()


# In[74]:


gdf_luzern.shape


# #### type

# Diese Spalte gibt bestimmte Details zum Gebäude an. Ist allerdings nicht sehr zuverlässig, wie zB diese Suche zeigt: In Luzern haben nur drei Gebäude den Typ «university».

# In[75]:


gdf_luzern['type'].value_counts()


# In[76]:


gdf_luzern[gdf_luzern['type'] == 'university']


# Nichtsdestotrotz können wir dieses Attribut zB nutzen, um gewisse Gebäude beim Plotten farblich hervorzuheben.

# In[77]:


# Alle Gebäude
ax = gdf_luzern.plot(figsize=(15,10), color='lightgrey')

# Kirchen
gdf_luzern[gdf_luzern['type'] == "church"].plot(color='green', ax=ax)

ax.set_title("Kirchen in Luzern")


# In[ ]:





# In[ ]:





# In[ ]:





# ## 3. via OSMnx

# OSMnx ist eine alternative Möglichkeit, um Daten aus der Open Street Map zu laden.
# 
# Es ist eine Python-Bibliothek, die anhand von selektiven Angaben
# - die ein Suchquery bei der Overpass-API generiert und
# - die Resultate zur praktischen Weiterverarbeitung aufbereitet
# 
# OSMnx-Dokumentation: https://osmnx.readthedocs.io/en/stable/
# 
# Beispiel-Notebooks zur Anwendung: https://github.com/gboeing/osmnx-examples/tree/main/notebooks
# 
# Hier lernen wir einige Möglichkeiten kennen, welche diese Library bietet.

# ## Datenabfrage: Boundaries

# OSMnx kann anhand eines einfachen Suchstrings die OSM durchsuchen und liefert uns so z.B. die Umrisse eines bestimmten geografischen Gebiets.
# 
# Die Funktion dafür heisst `geocode_to_gdf()`:

# In[6]:


gdf = ox.geocode_to_gdf("Aargau, Switzerland")


# Wir erhalten ein Geodataframe mit einer einzigen Zeile.

# In[7]:


gdf


# Diese Zeile entspricht einer geografischen Einheit auf Open Street Map.
# 
# Wir erkennen das zB wenn wir auf OSM nach der `osm_id` suchen: https://www.openstreetmap.org/relation/1686359

# In[8]:


Image("dataprojects/osm/ag.png")


# Mit unserem Geodataframe können wir nun alles machen, was wir wollen. zB plotten:

# In[9]:


gdf.plot()


# #### Mehrere Gebiete abfragen
# 
# Mit einer Liste von Suchstrings können wir ein Geodatenframe erstellen, das mehrere Einträge enthält.

# In[10]:


places = [
    "Kreis 1, Zürich, Switzerland",
    "Kreis 2, Zürich, Switzerland",
    "Kreis 3, Zürich, Switzerland",
    "Kreis 4, Zürich, Switzerland",
    "Kreis 5, Zürich, Switzerland",
    "Kreis 6, Zürich, Switzerland",
    "Kreis 7, Zürich, Switzerland",
    "Kreis 8, Zürich, Switzerland",
    "Kreis 9, Zürich, Switzerland",
    "Kreis 10, Zürich, Switzerland",
    "Kreis 11, Zürich, Switzerland",
    "Kreis 12, Zürich, Switzerland"
]
gdf = ox.geocode_to_gdf(places)


# In[11]:


gdf.plot()


# #### Präzise Suche
# 
# Manche Suchstrings können missverständlich sein. ZB «Zürich, Switzerland»: Ist hier die Stadt oder der Kanton gemeint? Um Missverständnisse auszuschliessen, können wir unsere Spezifikation in einem Dictionary präzisieren:

# In[12]:


gdf = ox.geocode_to_gdf(
    {
        "state": "Zürich",
        "country": "Switzerland"
    }
)


# In[13]:


gdf.plot()


# #### Koordinatensystem
# 
# Wichtig: Sobald wir mit diesen Daten kartografisch irgendwas sinnvolles machen wollen, sollten wir sie in ein passendes Koordinatensystem umprojizieren.

# In[14]:


gdf.crs


# In[15]:


gdf = gdf.to_crs(epsg=21781)


# In[16]:


gdf.plot()


# ## Datenabfrage: Netzwerke

# Um ein Strassennetzwerk aus OSM zu laden, machen wir zwei Schritte statt nur einen.

# #### 1. Graph erstellen
# 
# OSMnx lädt die Daten zuerst in einen sogenannten Graph (des Typs `networkx`). Die Funktion dazu heisst `graph_from_place():`:

# In[17]:


G = ox.graph_from_place("Luzern, Switzerland", network_type="drive")


# Diesen Graph können wir mix OSMnx auch bereits direkt plotten:

# In[18]:


ox.plot_graph(G)


# Um in Geopandas damit zu arbeiten, müssen wir den Graph konvertieren mit `graph_to_gdfs()`:

# In[19]:


gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)


# Wir erhalten zwei Geodataframes, eines mit den Punkten (nodes) und eines mit den Linien (edges):

# In[20]:


gdf_nodes.head()


# In[21]:


gdf_edges.head()


# ### BBox statt Suchstring

# Statt mit einem Suchstring («Luzern, Switzerland») können wir die Datensuche auch mit einer bounding box eingrenzen:

# In[22]:


north, south, east, west = 47.06954, 47.03474, 8.2715, 8.33184


# Die Funktion heisst dann leicht anders: `graph_from_bbox()`

# In[23]:


G = ox.graph_from_bbox(north, south, east, west, network_type="drive")


# In[24]:


ox.plot_graph(G)


# ### Metainformationen

# In der Open Street Map hat es nebst den reinen Geoinformationen – so genannte «nodes» (Punkte), «ways» (Linien) und «relations» (zusammengefasste nodes und ways) – auch eine Menge Metainformationen. Diese kann man mit OSMnx abfragen.

# #### Netzwerktypen

# Statt nach `network="drive"` (fahrbare Strassen) können wir zum Beispiel auch nach anderen Strassennetzen suchen:
# 
# - `drive` - get drivable public streets (but not service roads)
# - `drive_service` - get drivable streets, including service roads
# - `walk - get all` streets and paths that pedestrians can use (this network type ignores one-way directionality)
# - `bike - get all` streets and paths that cyclists can use
# - `all - download` all non-private OSM streets and paths
# - `all_private` - download all OSM streets and paths, including private-access ones
# 

# #### Filter

# Und wir können die Suche mit so genannten Filtern weiter eingrenzen. ZB nur auf Autobahnen, mit `custom_filter=`:

# In[25]:


G = ox.graph_from_place("Aargau, Switzerland", network_type="drive", custom_filter='["highway"~"motorway"]')


# In[26]:


gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
gdf_edges = gdf_edges.to_crs(epsg=21781)


# Wir können die aargauer Autobahnen plotten, zB indem wir zusätzlich noch die Umrisse des Kantons holen:

# In[27]:


gdf_ag = ox.geocode_to_gdf("Aargau, Switzerland")
gdf_ag = gdf_ag.to_crs(epsg=21781)


# In[28]:


ax = gdf_ag.plot(color="lightgrey", linewidth=1, edgecolor='black')
ax.set_title("Autobahnen im AG")
gdf_edges.plot(color='red', ax=ax)


# Wie kommt man auf diese Filterwörter? Die Antwort lautet: Es sind so genannte Tags, die in OSM hinterlegt sind.

# #### Tags

# Schauen wir uns zunächst unser Suchergebnis zu den Autobahnen nochmals an.
# 
# Unser Filter hiess: '["highway"~"motorway"]'
# 
# Im Geodataframe finden wir diese Begriffe wieder:
# - Es gibt eine Spalte namens «highway»
# - Die Einträge darin heissen «motorway» oder ähnlich.

# In[29]:


gdf_edges.head()


# Wo diese Metainformation herkommt, erkennen wir auf der Online-Version von OSM, wenn wir eines der Features aus unserem Geodataframe dort abrufen: https://www.openstreetmap.org/way/827816284

# In[30]:


Image("dataprojects/osm/a3.png")


# Das betreffende Geoelement wurde auf OSM als «highway» getagged und hat, mit der Unterkategorie «motorway».
# 
# Das OSM-Wiki verrät uns, was es alles für Typen von highways gibt: https://wiki.openstreetmap.org/wiki/Key:highway?uselang=en
# 
# Und auch sämtliche anderen Metainformationen zu diesem Autobahnteilstück («lanes», «oneway», «maxspeed») finden wir in unserem Geodataframe wieder.

# #### Andere Netzwerke

# Welche anderen Tags können wir nutzen, um nach bestimmten Geofeatures zu suchen?
# 
# Auf dem OSM-Wiki gibt es dazu eine ellenlange Liste: https://wiki.openstreetmap.org/wiki/Map_features
# 
# - `"aerialway"`: Seilbahnen
# - `"amenity"`: Jegliche Art von Objekt mit einer speziellen Funktion: `~"bar"`, `~"library"`, `~"charging_station"`, etc.
# - `"boundary"`: eine Umgrenzung. In Kombination nutzbar mit `"admin_level"`
# - `"building"`: ein Gebäude. zB `~"mosque"`, `~"train_station"`, `~"parking"`, `~"stadium"`, etc.
# - `"landuse"`: Wie ein bestimmtes Landstück genutzt wird, zB `~"farmland"`
# - `"natural"`: Elemente der Natur, zB `~"glacier"`, `~"beach"`, etc.
# - etc.
# 
# So können wir zB statt nach Strassen nach Eisenbahnen suchen:

# In[31]:


G = ox.graph_from_place("Aargau, Switzerland", custom_filter='["railway"~"rail"]')


# In[32]:


ax = gdf_ag.plot(color="lightgrey")
ax.set_title("Eisenbahnen im AG")

gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
gdf_edges.to_crs(21781).plot(ax=ax)


# In[ ]:





# In[ ]:





# ## Datenabfrage: Geometrien

# Bis jetzt haben wir (Strassen-)netzwerke abgefragt. Mithilfe der auf OSM hinterlegten Tags können wir aber auch sämtliche Geo-Elemente jeglicher herunterladen, die in einem bestimmten Gebiet vorhanden sind.

# ### Gebäude

# Dazu gibt es die Funktion `geometries_from_place()`. Sie benötigt:
# - eine geografische Eingrenzung der Suche ("place")
# - eine (Reihe von) Tags, nach denen gesucht werden soll.

# In[33]:


place = "Wettingen, Switzerland"
tags = {"building": True}
gdf_bldg = ox.geometries_from_place(place, tags)


# In Wettingen sind zB über 3000 Gebäude erfasst:

# In[34]:


gdf_bldg.shape


# Da es ziemlich viele Tags gibt, die sonst noch mit diesen Gebäuden verknüpft sind, erhalten wir ein ziemlich breites GDF:

# In[35]:


gdf_bldg.columns


# In[36]:


gdf_bldg.head(5)


# Wir sehen hier auch, dass das Geodatenframe drei übergeordnete Indizes hat.
# 
# Die ways (Pfade), relations (Sammlungen) und nodes (Punkte) sind separat aufgeführt.

# In[37]:


gdf_bldg.index.get_level_values('element_type').value_counts()


# Wir können uns aus diesem Multi-Index zB die Pfade heraussuchen.

# In[38]:


gdf_bldg = gdf_bldg[gdf_bldg.index.get_level_values('element_type') == 'way']


# In[39]:


gdf_bldg.head(2)


# Jedes Gebäude hat einen Pfad, das dessen Umriss angibt. Wir können so die Geäbude plotten:

# In[40]:


gdf_bldg = gdf_bldg.to_crs(epsg=21781)
gdf_bldg.plot(figsize=(10,10))


# ## Anwendungen

# Nachfolgend ein paar Beispiele, was wir in Geopandas mit den Datenabfragen anstellen können.

# ### Plots von mehreren Datenabfragen

# Wir haben das schon weiter oben gesehen. Mit `ax=...` können wir mehrere Plots übereinanderlegen:

# In[41]:


# Abfrage und Plot der Gemeindegrenze
gdf_we = ox.geocode_to_gdf("Wettingen, Switzerland").to_crs(epsg=21781)
ax = gdf_we.plot(color='lightgrey', figsize=(10, 10))

# Plot der Gebäude (auf "ax")
gdf_bldg.plot(figsize=(10,10), ax=ax)


# ### Abgefragte Daten filtern

# Wie bereits erwähnt: Wir haben ein riesenbreites Geodataframe mit zig Metadaten.

# In[42]:


gdf_bldg.head(2)


#  Wir können zB all die Gebäude heraussuchen, die gleichzeitig auch eine «amenity» eines bestimmten Typs sind.

# In[43]:


gdf_schools = gdf_bldg[gdf_bldg['amenity'] == 'school']


# Das Ergebnis als Plot:

# In[44]:


# Gemeindegrenze
ax = gdf_we.plot(linewidth=0.5, edgecolor='black', color='lightgrey', figsize=(20, 20))

# Alle Gebäude
gdf_bldg.plot(color='grey', ax=ax)

# Schulen
gdf_schools.plot(color='red', ax=ax)


# Nun haben wir allerdings ein Problem: In Wettingen gibt es noch mehr Schulen als hier eingezeichnet sind.

# ### Daten ergänzen

# Das Problem scheint zu sein: Einige der Schulen wurden zwar als "amenity": "school" kategorisiert, aber nicht als "building" :-/
# 
# Wir holen uns deshalb von der OSM nochmals alle Geometrien raus, die als "school" getaggt wurden (aber nicht zwangsläufig auch als Gebäude!

# In[45]:


place = "Wettingen, Switzerland"
tags = {"amenity": "school"}
gdf_schools2 = ox.geometries_from_place(place, tags).to_crs(epsg=21781)


# Ein Beispiel für einen solchen Eintrag ist das Schulhaus Altenburg:

# In[46]:


gdf_schools2[gdf_schools2['name'] == "Altenburg"]


# Es wurden also gewisse Areale als Schule getaggt, aber nicht die dortigen Gebäude.
# 
# Was das heisst, sieht man, wenn man die Areale zum obigen Plot hinzufügt.

# In[47]:


# Gemeindegrenze
ax = gdf_we.plot(linewidth=0.5, edgecolor='black', color='lightgrey', figsize=(20, 20))

# Alle Gebäude
gdf_bldg.plot(color='grey', ax=ax)

# Schulen => aus Gebäuden
gdf_schools.plot(color='red', ax=ax)

# Schulen => aus Amenities
gdf_schools2.plot(color='blue', linewidth=0.5, alpha=0.3, edgecolor='black', ax=ax)


# #### Lösungsansatz:
# 
# Gebäude, die innerhalb der Schul-Areale liegen, umklassifizieren.
# 
# Dazu nutzen wir die Funktion `unary_union`, um alle Schul-Areale zu einer gemeinsamen Shape zusammenzufassen.

# In[48]:


gdf_schools2.unary_union


# Danach filtern wir die Gebäude in unserem `gdf_bldg` danach, ob sie innerhalb dieser Shape liegen.
# 
# Die passende Relation dazu heisst `within()`.
# 
# Bei allen Treffern schreiben wir in der Spalte «amenity» neu überall "school" rein.

# In[49]:


gdf_bldg.loc[gdf_bldg['geometry'].within(gdf_schools2.unary_union), "amenity"] = "school"


# Letzter Schritt: Wir filtern nochmals das Gebäude-GDF, diesmal inklusive der neu klassifizierten Einträge:

# In[50]:


gdf_schools = gdf_bldg[gdf_bldg['amenity'] == 'school']


# Jetzt haben wir eine vollständige (?) Sammlung aller Schulgebäude.

# In[51]:


# Gemeindegrenze
ax = gdf_we.plot(linewidth=0.5, edgecolor='black', color='lightgrey', figsize=(20, 20))

# Alle Gebäude
gdf_bldg.plot(color='grey', ax=ax)

# Schulen
gdf_schools.plot(color='red', ax=ax)


# ### Räumliche Berechnungen

# Sobald wir Daten als Geodataframe vorliegen haben, können wir allerlei Berechnungen durchführen.
# 
# #### Zum Beispiel:
# 
# Wie weit liegt ein bestimmtes Gebäude von der nächsten Bushaltestelle entfernt?
# 
# Um das zu beantworten, laden wir uns aus der OSM die Busstationen in Wettingen.

# In[52]:


place = "Wettingen, Switzerland"
tags = {"highway": "bus_stop"}
gdf_stops = ox.geometries_from_place(place, tags=tags).to_crs(epsg=21781)


# In[53]:


gdf_stops.shape


# In[54]:


gdf_stops.head()


# Plot auf unserem Gemeindeplan mit den Gebäuden:

# In[55]:


# Gemeindeumriss
ax = gdf_we.plot(linewidth=0.5, edgecolor='black', color='#EEEEEE', figsize=(20, 20))

# Gebäude
gdf_bldg.plot(color='#999999', ax=ax)

# Bushaltestellen
gdf_stops.plot(color='blue', markersize=25, ax=ax)


# Wir können die Funktion `.distance()` nutzen, um die Distanz zwischen zwei Shapes zu berechnen.
# 
# Wenn wir diese Funktion auf ein ganzes Dataframe anwenden, erhalten eine Liste von Distanzen: von jedem Element im DF zur angegebenen Shape.
# 
# Hier zum Beispiel: die Distanzen sämtlicher Bushaltestellen zum ersten Eintrag im Gebäude-GDF:

# In[56]:


gdf_stops.distance(gdf_bldg.iloc[0]['geometry']).head(10)


# Wenn wir aus dieser Liste das Minimum auswählen, erhalten wir die Distanz von diesem Gebäude zur *nächsten* Bushaltestelle:

# In[57]:


gdf_stops.distance(gdf_bldg.iloc[0]['geometry']).min()


# Diese Berechnung führen wir nun mit sämtlichen Gebäuden durch. Dazu nutzen wir `apply()`.
# 
# Das Ergebnis speichern wir in einer neuen Spalte.

# In[58]:


gdf_bldg['distance_next_stop'] = gdf_bldg['geometry'].apply(lambda bldg: gdf_stops.distance(bldg).min())


# Die Distanzen sind folgendermassen verteilt:

# In[59]:


gdf_bldg['distance_next_stop'].hist(bins=50)


# Wir können nun auf unserem Plot zB die Gebäude einfärben entsprechend der Distanz zur nächsten Bushaltestelle.
# 
# Das Limit für die Colormap setzen wir auf 500 Meter, damit man die Unterschiede gut erkennt.

# In[60]:


# Gemeindeumrisse
ax = gdf_we.plot(linewidth=0.5, edgecolor='black', color='#000000', figsize=(20, 20))

# Gebäude, eingefärbt entsprechend der Distanz
gdf_bldg.plot(ax=ax, column='distance_next_stop', cmap='autumn_r', vmin=0, vmax=500)

ax.set_title("Wettingen AG: Nähe zur Bushaltestelle")


# In[ ]:





# In[ ]:




