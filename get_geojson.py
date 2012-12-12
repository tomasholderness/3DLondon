#!/usr/bin/env python

# get_geojson.py - CGI script to get UKMap building geom/heights from PostGIS and return as GeoJson strings.
# Tested with lighttpd.

# Note: this is just a test script, it would be more efficient to implement this in a real web framework (i.e. GeoDjango) in WSGI format.

# Copyright Tom Holderness 2012.
# Released under BSD license (see LICENSE.txt) 
# https://github.com/talltom/3DLondon

__author__='Tom Holderness'
__year__='2012'
__version__ = "0.1"

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import json
import psycopg2

# Get bbox coords from URL query, with a little minimal error checking
fs = cgi.FieldStorage()
if 'bbox_wkt' not in fs:
	print "Content-type: text/html"
	print
	print "<h1>Error</h1>"
	print "bbox_wkt was not found in URL query string."
else:
   bbox_wkt = fs['bbox_wkt'].value

# Database connection
conn = psycopg2.connect("dbname=ukmap_london user=postgres password=postgres")

# Database cursor
cur = conn.cursor()

# Query
cur.execute('SELECT row_to_json(fc) FROM ( SELECT \'FeatureCollection\' As type, array_to_json(array_agg(f)) As features FROM (SELECT \'Feature\' As type, ST_AsGeoJSON(ST_Transform(lg.the_geom,4326))::json As geometry, row_to_json((SELECT l FROM (SELECT height) As l)) As properties FROM "3DLondon" As lg WHERE ST_Within(lg.the_geom, ST_Transform(ST_GeomFromText(%s,4326),27700)) LIMIT 100000) As f )  As fc;',[bbox_wkt])
array = cur.fetchall()

# Return data as GeoJSON
print "Content-type: application/json\n"
# Format JSON data
jsondata = json.dumps(array[0])
# Hack to remove Ptthon list brackets
jsondata = jsondata[2:-2]
# Remove escaped strings
jsondata = jsondata.replace("\\","")
# Print the data
print jsondata
