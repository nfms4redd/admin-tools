#! /usr/bin/env python

import sys
import portal 
import argparse

parser = argparse.ArgumentParser(description='Modify layer in layers.json')
parser.add_argument('--id', help="Id of the layer to be modified", required=True)
args = parser.parse_args()

layerId = args.id;
wmsLayerId = "wms-" + layerId

root = portal.readPortalRoot()

wmsLayer = portal.findLayerById(root["wmsLayers"], wmsLayerId)
if wmsLayer is not None:
  root["wmsLayers"].remove(wmsLayer);

portalLayer = portal.findLayerById(root["portalLayers"], layerId)
if portalLayer is not None:
  root["portalLayers"].remove(portalLayer);

group = portal.findGroupContainingLayer(root, layerId)
if (group is not None):
  group.get("items").remove(layerId)

portal.writePortalRoot(root)