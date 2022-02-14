# RoadAccidentsSwitzerland
An analysis of swiss road accidents between 2011 and 2020. [The code can be found here](RoadAccidents_Code.ipynb). 

## Ausgangslage
In meiner Arbeit möchte ich die Schweizer Strassenunfälle der letzten zehn Jahre analysieren und clustern, um Hotspots zu finden und zu eruieren, welche Gebiete gefährlicher und welche Gebiete weniger gefährlich wurden. **Arbeitstitel: «Die gefährlichste Strasse der Schweiz»**. In einer «traditionell»-journalistischen Recherche mit Betroffenen und Behörden will ich anschliessend herausfinden, warum Gebiete gefährlicher wurden, was man von anderen Orten lernen kann und wie es ist, beispielsweise an der gefährlichsten Strasse der Schweiz zu leben. Wobei da definiert werden muss, was die gefährlichste Strasse ist. Dazu muss zb vermutlich das Verkehrsaufkommen berücksichtigt werden. 

## Ausgangsthese
Ich gehe davon aus, dass die Zahl der Unfälle über die Jahre einigermassen stabil bleibt (mit einer Abnahme die letzten Jahre wegen Corona), aber die Unfallorte ändern. Ich möchte diese Orte identifizieren, unter anderem um den Leser auf Gefahrenstellen aufmerksam zu machen. Ich gehe davon aus, dass die Politik solche neuralgischen Punkte kennt, aber vielleicht hat der Artikel/die mögliche Artikelserie trotzdem einen Impact.

## Daten
Das Bundesamt für Strassen (Astra) hat die mit Abstand beste Datenlage für meine Geschichte. Das Astra publiziert [auf dem Geoportal des Bundes eine Unfallkarte](https://map.geo.admin.ch/?topic=vu&lang=de&bgLayer=ch.swisstopo.pixelkarte-grau&layers=ch.astra.unfaelle-personenschaeden_alle&layers_timestamp=99990101&catalogNodes=1318), welche die Unfälle mit Personenschaden seit 2011 geografisch nach bestimmten Themen darstellt. Darin werden alle der Polizei gemeldeten Unfälle auf öffentlichen Strassen oder Plätzen erfasst, in die mindestens ein Motorfahrzeug, ein Fahrrad oder ein fahrzeugähnliches Gerät verwickelt ist. [Hier sind die Daten im Repository zu finden](Data/RoadTrafficAccidentLocations.csv). Die Daten werden vom Astra [als CSV, JSON und XTF zur Verfügung gestellt](https://data.geo.admin.ch/ch.astra.unfaelle-personenschaeden_alle/). Der entsprechende Rohdatensatz wird zudem auf dem [Open-Government-Data-Portal des Bundes](https://opendata.swiss/de/dataset/strassenverkehrsunfallorte) und als [verlinkbare Daten](https://www.geo.admin.ch/de/geo-dienstleistungen/geodienste/linkeddata.html) zur Verfügung gestellt. [Für Interessierte gibt es hier die ausführliche Dokumentation](Strassenverkehrsunfallort_Modellbeschreibung.pdf). 

**Der Datensatz fürs Jahr 2021 wird «zwischen Anfang und Mitte März» publiziert**, wie mir das Astra sagte. 

Daneben habe ich das Amtliche Verzeichnis der Strassen genutzt, um den Unfalldaten Strassen zuzuordnen. Dieses ist [im Repository](Data/pure_str.csv) oder [in diesem Zip-File abgelegt](https://data.geo.admin.ch/ch.swisstopo.amtliches-strassenverzeichnis/csv/2056/ch.swisstopo.amtliches-strassenverzeichnis.zip).

## Vorgehen
Meine Arbeit besteht aus 4 Schritten:
1. Quantitative Analyse der Daten. In welchen Jahren wie viele Unfälle mit Personenschäden, etc. Die Möglichkeiten sind zahlreich und ich werde mich auf einige wenige fokussieren. 
2. Danach die Unfalldaten Adressen zuordnen um herauszufinden, welches die gefährlichste Strasse der Schweiz ist (wie das definiert ist, ist noch nicht sicher)
3. Visualisierung der Daten auf einer Schweizer Karte. 
4. Finden von Protagonisten, um aus der Daten-Geschichte einen Blick-Artikel zu machen.

## Einschätzung von Aufwand/Ertrag vor Beginn des Projektes
Für die Arbeit sind 5 Tage vorgesehen. Ich denke, dass ich länger brauchen werde. Ein Zeitlimit setzte mich mir nicht. Aber mein Glaube und auch Ziel ist, dass die Daten derart gut sind, dass sich daraus diverse Geschichten machen lassen. Wenn mein Code mal passt, kann ich alles Mögliche analysieren und das auch jedes Jahr von neuem Nutzen. Darum das Credo: Einmal viel Aufwand, für lange viel Ertrag. 

## Bezeichnung der Knackpunkte des Projektes
Das Beschaffen der Daten war einfach. Die quantitative Analyse brauchte dann einige Zeit. Auch wenn wir die Auswertungen auf die eine oder andere Weise schon vorgenommen hatten, verbrachte ich viele Stunden in unseren Dokumentationen und auf Stackoverflow, um Lösungen für diverse Probleme zu finden.
**Besonders schwierig war es dann, den Unfalldaten Adressen zuzuordnen. Respektive gelang mir dies nicht**. Ich hatte Längen- und Breitengrade der Unfallpunkte, aber konnte diese nicht so aufbereiten, dass ich sie vernünftig clustern und daraus quantiative Auswertungen machen konnte. **Auch das visualisieren der Daten auf einer Karte stellte sich als Herausforderung dar, die letztendlich nur halb zufriedenstellend gelöst werden konnte**. Beim Gruppieren nach Koordinaten kam es zu Wiederholungen, wie ich beim Kontrollieren feststellte. Die Erklärung zu den Problemen gibt es etwas detaillierter [hier](Problems).

## Gespräche mit Briefing-Personen
- Ich habe mehrmals mit **Gerhard Schuhwerk, Bereichsleiter Anwendungen und Datenbewirtschaftung beim Astra**, gesprochen. Er hat mir Informationen zum Datensatz gegeben, beispielsweise, was der Unterschied zwischen den Variablen «Unfälle mit Fussgängerbeteiligung» und «Unfalltyp ‘Fussgängerunfall’ sind. 
 
- Rund eine Stunde habe ich mit **Dr. Clemens Kielhauser, Kompetenzbereich Verkehrsinfrastruktur der Berner Fachhochschule**, gesprochen. Es ging darum, wie ich meine Koordinaten dem Strassennetz zuordnen kann. Er macht mit seinen Studenten ebenfalls Unfallanalysen und hat mir gesagt, dass Geopandas nicht das richtige Werkzeug sei, riet mir zu GIS-Datenbanksystemen und sagte mir, dass eine Studentin von ihm dasselbe wie ich gemacht habe, allerdings auf eine Art, zu der ich nicht in der Lage war. Demnach müsste  ich Kreuzungen und Strassenstücke bilden und dann meinen Algorithmus nach Unfallpunkten suchen lassen, die sich in einem gewissen Radius befinden. So soll die Zuteilung funktionieren. Ich wusste aber nicht wie ich das technisch lösen kann und die Studentenarbeit konnte ich noch nicht einsehen, weil sie offenbar vom Astra noch gebraucht wird. Zudem sprachen wir noch darüber, wie sich die These «gefährlichste Strasse der Schweiz» am besten definieren lässt und Kielhauser riet mir dazu, dafür die Unfalldichte als Raster darüberzulegen. 
 
- Ebenfalls rund eine Stunde habe ich mit **Stefan Graf, Programm-Manager Bildung bei Esri Schweiz**, gesprochen. Esri stellt Geoinformationssysteme her und er gab mir eine (Schul)Lizenz für ihre Software, mit der ich diverse Auswertungen machen kann. Aus Zeitgründen kam ich bisher nicht dazu, diese zu lernen und anzuwenden, das steht dann nach Abgabe der Arbeit auf dem Programm. Ich hatte mit Esri gesprochen weil ich realisierte, mit meinen Programmierfähigkeiten nicht mein Problem lösen zu können. Zuerst versuchte ich es mit der Freeware QGIS, kam damit aber nicht zurecht, weswegen ich bei Esri anfragte. 
 
- Es gab auch Mailverkehr mit anderen  Experten, beispielsweise dem [*GIS-Experten Ralph Straumann*](https://www.ralphstraumann.ch/), um herauszufinden, wie ich Unfalldaten sinnvoll clustern kann. 

- Daneben verschiedene Gespräche mit Dozenten und Kommilitonen – hier sei **besonders Marlen Hämmerli hervorgehoben**, die mir zeigte, wie ich Koordinaten von EPSG2056 (LV95) zu EPSG4326 (WSG84) umrechnen kann. Aber auch Barnaby Skinner, Simon Schmid und Ruben Schönenberger standen für wertvolle Inputs bereit.

## Ergebnis und Ausblick
Ich habe keinen Artikel abgegeben. Das hatte ich auch nicht geplant, weil die neusten Unfalldaten in wenigen Wochen erscheinen und es dann mehr Sinn ergibt. Um allerdings dann den gewünschten Artikel schreiben zu können, muss es mir gelingen, den Unfalldaten Strassenpunkten zuzuordnen. Nur dann kann ich Auswertungen machen, die über «Vergleich von Zahl der Radfahrunfällen über die Jahre» etc hinausgehen. Dafür werde ich einerseits die GIS-Software von ESRI ausprobieren und andererseits nochmal versuchen, die Studienarbeit von Dr. Kielhauser zu erhalten. Falls das nicht gelingt, werde ich einen abgespeckteren Artikel schreiben, in dem ich verschiedene quantitative Analysen vornehme und diese dann durch Recherche vor Ort in einen oder mehrere Artikel für Blick verwandle. Zudem will ich noch versuchen ob es irgendwie möglich ist, bei den Hotspots die doppelten Datenpunkte zu vermeiden.

## Geplanter Artikel
###Titel: «Die gefährlichste Strasse der Schweiz»
###Lead: In der Schweiz gab es im Jahr 2021 xx Unfälle. Die meisten davon an der YY-Strasse. Blick ist vorbeigefahren und hat mit Betroffenen gesprochen. Und zeigt Lösungen auf, wie der Abschnitt sicherer gemacht werden kann. 
###Storyline: Anhand der Auswertung der Unfalldaten wird die gefährlichste Strasse der Schweiz gefunden (im Vergleich zur Unfalldichte). Wir vergleichen die Daten mit vorherigen Jahren und finden auch Strassen, die sicherer wurden. Anhand davon lässt sich eventuell ableiten, wie auch die gefährlichste Strasse 2021 sicherer gemacht werden könnte. Eine weitere Geschichte wird sein, mit Unfallopfern, Anwohnern, Polizisten, Behörden zu sprechen. 

##Zusammenfassung der durch die Daten belegten Fakten in Form eines Textes
Die Daten die ich für meinen Artikel verwendet habe zeigen: Es gab zwischen 2011 und 2020 insgesamt 178’217 Verkehrsunfälle mit Personenschäden in der Schweiz. Davon forderten 2395 – 1,3 Prozent – ein oder mehrere Todesopfer. Die Zahl der Unfälle bleibt dabei relativ stabil. Zurückgegangen sind sie im Jahr 2020, was auf Corona zurückzuführen sein dürfte. Mehr Home-Office, weniger Touristen, die durch die Schweiz fahren sind mögliche Gründe. Der Trend dürfte auch im Jahr 2021 anhalten. Etwas genauer angeschaut habe ich die Fussgängerunfälle. Davon gab es zwischen 2011 und 2020 20’580. Rund 30 Prozent (6’222) davon waren schwer oder sogar tödlich. Das dünkt mich viel, besonders, weil es Massnahmen geben müssete, die so etwas verhindern könnten. Mehr Fussgängerstreifen oder Ampeln zum Beispiel. Diesen Aspekt werde ich definitiv noch vertiefen, sobald ich herausfinde, wo die neuralgischen Stellen sind. 


## Arbeitsprotokoll

### 6. bis 19. September 2021
Die Idee, die Strassenunfalldaten des Bundes zu analysieren, hatte ich recht schnell gefasst. Ich fand den Datensatz im Vorfeld der Vorbereitung auf den CAS und war faszinizert von den Möglichkeiten. Gespräche mit den Dozenten und das im Bootcamp gelernte bestätigten mir, dass sich der Datensatz gut als Abschlussarbeit eignet. 

### 30. Oktober
Datensatz heruntergeladen, in Dokumentation eingelesen. 

### 1. November
Erstes Gespräch mit Gerhard Schuhwerk, Bereichsleitung Anwendungen und Datenbewirtschaftung beim Astra, Ideenaustausch. 

### 2. + 3. November
Erste quantitative Auswertungen gemacht. Versucht zu eruieren, welche Parameter spannend sein können. 

### Restlicher November
Weitere Auswertungen gemacht, Shapefiles gesucht für später. Hat mich aber nicht voran gebracht in meinem Ziel, die Koordinaten auf einer Karte abzubilden. Nach Evaluation meiner Auswertungen entschieden, mich einerseits auf die tödlichen Strassenunfälle generell, andererseits auf tödliche und schwere Unfälle mit Fussgängerbeteiligung zu fokussieren. Erste Plots gemacht. 

### Dezember
Wegen Daily Business kaum Zeit gehabt für die Arbeit. Weil die Daten schon oft benutzt wurden, war meine Idee, die Daten auf eine innovative Art zu clustern. Habe den Monat vor allem damit zugebracht, nach GIS-Gruppen zu suchen, die mir Inputs liefern können. Zudem gemerkt, dass ich meine Koordinaten von EPSG2056 (LV95 vom Bund) nach EPSG4326 (WSG84) umrechnen muss. 

### 3. Januar 2022
Zweites Gespräch mit Gerhard Schuwerk vom Astra. Er sagte mir, Astra hat die Koordinaten nur als LV95-Datenpunkte. Zudem erklärte er mir weitere Nuancen im Datenset, etwa den Unterschied zwischen dem Accidentype at8 (Fussgängerunfall) und "AccidentInvolvingPedestrian".

### 7. Januar
Gespräch mit Kommilitonin Marlene Hämmerli. Sie hat mir gesagt, ihre ihren Code mit mir geteilt, in dem sie die Daten erfolgreich von CHLV95 nach WSG84 transformierte. Hat auch bei mir funktioniert. 

### 15. Januar
Probierte Googles Geocoding AP als Möglichkeit, um den Unfalldaten Adresspunkte zuzuordnen. War aber nichts für mich, da die Schnittstellennutzung nicht gratis ist und bei meiner Zahl von Datensätzen zu viel kosten würde. 

### 15. Januar-18. Januar
Amtliche Verzeichnis der Strassen mit Unfalldaten-File gemerged. Hat geklappt, aber Resultate falsch (im Code-File genauer erklärt). 

### 19. Januar
Mit Patrick Ibele, Coordination, Geo-Information and Services (COGIS) bei Swisstopo gesprochen. Er sagte, das Strassenverzeichnis funktioniere nicht für das, was ich will. Für eine automatisierte Zuordnung wie ich sie wollte, könne eine Desktop-GIS nützlich sein. 

### 19. Januar
Endlich Erfolg bei Suche nach GIS-Fachpersonen. 1h Call mit Dr. Clemens Kielhauser von der FH Bern. Weitere Infos unter «Gespräche mit Briefing-Personen». 

### 19. Januar
Download und Ausprobieren der Open-Source-GIS-Lösung QGIS. War mir aber zu umfangreich. 

### 20. Januar
Nachdem Strassenverzeichnis-Merging gescheitert war und ich Kielhausers Lösung nicht umsetzen konnte, versuchte ich, die Unfalldaten anders Adressen zuzuordnen. Auf Nominatim (Geocoder) gestossen. Das war aber sehr langsam und crashte irgendwann. Versuch abgebrochen. 

### 21. Januar
Gespräch mit Stefan Graf von Esri. Stellte mir eine Studentenlizenz ihrer GIS-Software bereit. Tutorials geschaut, erste Versuche unternommen. Wurde mir aber rasch klar, dass ich es nicht schaffe, bis Abgabe die Software zu lernen und einzusetzen. Drohte, ob all der Inputs mein Ziel aus den Augen zu verlieren. 

### 22. Januar bis 25. Januar
Aufgegeben, die Unfalldaten Adressen zuzuordnen. Dadurch war der Versuch, die gefährlichste Strasse der Schweiz zu finden, nicht mehr möglich. Stattdessen Fokus auf Visualisierungen (im Code Rubrik “Displaying results on map”). Mit Library Plotly in Geopandas versucht, hat geklappt, aber Ergebnis nicht zufriedenstellend.

### 3. bis 6. Februar
Über einen Kollegen auf die Library Folium gestossen. Damit konnte ich die Unfallpunkte visualisieren. 
### 8. Februar
Gespräch mit Barnaby Skinner. War ziemlich in der Krise, weil meine Arbeit so viele Probleme hatte und ich mein Ziel nicht erreichen konnte. Er hat mich beruhigt. 

### 8. Februar
Eine Möglichkeit gefunden, Unfall-Hotspots in Folium darzustellen. Das war, wenn auch nicht perfekt, so ähnlich dem, was ich von Beginn an plante. So sieht man, wenn man sich durch die Marker klickt, dass im Bezirk Altstetten seit 2011 die meisten tödlichen Unfälle im Schweizer Strassenverkehr geschahen. Leder festgestellt, dass es mehr Datenpunkte angibt, als es Unfälle sind. Mehr dazu im Bereich Knackpunkte. 

### 11 bis 14. Februar
Code cleanen, Dokumentation schreiben, Abgabe. 

