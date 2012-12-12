3DLondon
========

PostGIS/Python CGI and JavaScript functions to generate map of 3D buildings in London from UKMap data using LeafletJS and OSM Buildings.

* map.htm: HTML/JavaScript Leaflet and OSMBuildings front end, adds buildings in GeoJSON format which are within map bounding box.
* get_geojson.py: Simple CGI script to return GeoJSON of buildings from PostGIS within specified bounding box.

![Screenshot](https://raw.github.com/talltom/3DLondon/master/screenshot.png)
