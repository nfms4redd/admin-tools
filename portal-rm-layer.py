#! /usr/bin/env python

import sys
import portal 
import argparse

parser = argparse.ArgumentParser(description='Remove layer in layers.json')
parser.add_argument("--file", help="Path to the layers.json file (default /var/portal/layers.json)", default="/var/portal/layers.json", nargs='?')
parser.add_argument('--id', help="Id of the layer to be removed", required=True)
args = parser.parse_args()

layerId = args.id;
wmsLayerId = "wms-" + layerId

root = portal.readPortalRoot(args.file)

wmsLayer = portal.findLayerById(root["wmsLayers"], wmsLayerId)
if wmsLayer is not None:
  root["wmsLayers"].remove(wmsLayer);

portalLayer = portal.findLayerById(root["portalLayers"], layerId)
if portalLayer is not None:
  root["portalLayers"].remove(portalLayer);

group = portal.findGroupContainingLayer(root, layerId)
if (group is not None):
  group.get("items").remove(layerId)

portal.writePortalRoot(root, args.file)
