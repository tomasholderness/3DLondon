#!/usr/bin/env python

#http://mail.python.org/pipermail/tutor/2002-September/017255.html

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import json
import psycopg2

# Get bbox coords from URL query
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
#cur.execute('SELECT row_to_json(fc) FROM ( SELECT \'FeatureCollection\' As type, array_to_json(array_agg(f)) As features FROM (SELECT \'Feature\' As type, ST_AsGeoJSON(ST_Transform(lg.the_geom,4326))::json As geometry, row_to_json((SELECT l FROM (SELECT height, "wallColor") As l)) As properties FROM "3DLondon" As lg WHERE ST_Within(lg.the_geom, ST_Transform(ST_GeomFromText(%s,4326),3857)) LIMIT 100000 ) As f )  As fc;',[bbox_wkt])
cur.execute('SELECT row_to_json(fc) FROM ( SELECT \'FeatureCollection\' As type, array_to_json(array_agg(f)) As features FROM (SELECT \'Feature\' As type, ST_AsGeoJSON(ST_Transform(lg.the_geom,4326))::json As geometry, row_to_json((SELECT l FROM (SELECT height) As l)) As properties FROM "3DLondon" As lg WHERE ST_Within(lg.the_geom, ST_Transform(ST_GeomFromText(%s,4326),3857)) LIMIT 100000 ) As f )  As fc;',[bbox_wkt])
array = cur.fetchall()

# Return data as GeoJSON
print "Content-type: application/json\n"
#print 'callback(%s);' % (json.dumps(array[0]))
jsondata = json.dumps(array[0])
jsondata = jsondata[2:-2]
jsondata = jsondata.replace("\\","")
#print 'callback(' + jsondata + ');'

print jsondata
#print 'callback(%s);' % (jsondata)
