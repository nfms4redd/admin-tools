#! /usr/bin/env python

import sys
import portal
import argparse

def findByIdOrCreate(list, id):
  ret = portal.findLayerById(list, id)
  if ret is None:
    ret = {}
    list.append(ret)
  return ret

parser = argparse.ArgumentParser(description='Modify layer in layers.json')
parser.add_argument("--file", help="Path to the layers.json file", default="/var/layers.json", nargs='?')
parser.add_argument('--id', help="Id of the layer to be modified", required=True)
parser.add_argument('--url', help="URL of the GeoServer layer", required=True)
parser.add_argument('--wmsname', help="Name of the layer in geoserver", required=True)
parser.add_argument('--label', help="Name of the layer", required=True)
parser.add_argument('--group', help="Group the layer is to be added", required=True)

args = parser.parse_args()

layerId = args.id
baseUrl = args.url
wmsName = args.wmsname
label = args.label
groupId = args.group

root = portal.readPortalRoot(args.file)

wmsLayerId = "wms-" + layerId

wmsLayer = findByIdOrCreate(root["wmsLayers"], wmsLayerId)
wmsLayer["baseUrl"] = baseUrl
wmsLayer["wmsName"] = wmsName
wmsLayer["visible"] = True
wmsLayer["id"] = wmsLayerId

portalLayer = findByIdOrCreate(root["portalLayers"], layerId)
portalLayer["label"] = label
portalLayer["layers"] = [wmsLayerId]
portalLayer["id"] = layerId

portal.setLayerInGroup(root, groupId, layerId)

portal.writePortalRoot(root, args.file)
