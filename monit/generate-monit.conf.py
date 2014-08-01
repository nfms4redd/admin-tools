#! /usr/bin/env python

'''
This script produces configuration for the monit (monitrc
file) to check all the layers returned by a GetCapabilities.

The monit check will query a GetFeatureInfo on an image of 1x1
pixels, hence returning all the features (at least in GeoServer).
Note that this can also be very heavy for the server.

The script requires the GetCapabilities result in the standard
input and the following parameters:

- Server to access in the HOST check
- url of the geoserver instance, typically "/geoserver/namespace/wms?"

Usage:

generate-monit.conf.py "geo2.ambiente.gob.ar" "/geoserver/bosques_umsef_db/wms?"
'''

import xml.etree.ElementTree as ET
import sys
import urllib

server=sys.argv[1]
appUrl=sys.argv[2]

template = '''CHECK HOST $layername WITH ADDRESS $server 
        if failed
                port 80
                protocol http
                status 200
                request "$appUrlREQUEST=GetFeatureInfo&EXCEPTIONS=application/vnd.ogc.se_xml&BBOX=$minx,$miny,$maxx, $maxy&SERVICE=WMS&INFO_FORMAT=text/html&QUERY_LAYERS=$layername&FEATURE_COUNT=999999&Layers=$layername&WIDTH=1&HEIGHT=1&format=image/png&styles=&srs=EPSG:4326&version=1.1.1&x=0&y=0"
                content != "<ServiceException>"
        then alert'''

url = 'http://' + server + appUrl + 'service=WMS&request=GetCapabilities'
print 'Downloading GetCapabilities: ' + url
capabilities = urllib.urlopen(url)
document = capabilities.read()
capabilities.close()

root = ET.fromstring(document)
layers = root.findall('{http://www.opengis.net/wms}Capability/{http://www.opengis.net/wms}Layer/{http://www.opengis.net/wms}Layer')
for layer in layers:
	bbox = layer.findall("{http://www.opengis.net/wms}BoundingBox[@CRS='EPSG:4326']")[0]

	layerTemplate = template
	layerTemplate = layerTemplate.replace("$layername", layer.find("{http://www.opengis.net/wms}Name").text)
	layerTemplate = layerTemplate.replace("$server", server)
 	layerTemplate = layerTemplate.replace("$appUrl", appUrl)
        layerTemplate = layerTemplate.replace("$minx", bbox.attrib["minx"])
        layerTemplate = layerTemplate.replace("$miny", bbox.attrib["miny"])
        layerTemplate = layerTemplate.replace("$maxx", bbox.attrib["maxx"])
	layerTemplate = layerTemplate.replace("$maxy", bbox.attrib["maxy"])

	print layerTemplate

