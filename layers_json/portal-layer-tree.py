#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import argparse
import portal

def showGroupItems(root, items, indent):
  for item in items:
    if isinstance(item, basestring):
      portalLayer = portal.findLayerById(root["portalLayers"], item)
      if portalLayer:
        mapLayers = portalLayer["layers"]
        print('\t' * indent + item + " (" + ", ".join(mapLayers) + ")")
    else:
      print('\t' * indent + item.get("id"))
      showGroupItems(root, item.get("items"), indent+1)

parser=argparse.ArgumentParser(description='''Muestra el árbol de capas especificado en el fichero layers.json.''')
parser.add_argument("--file", help="Ruta al fichero layers.json file (por defecto /var/portal/layers.json)", default="/var/portal/layers.json", nargs='?')
args=parser.parse_args()

with open(args.file, "r") as file:
  root=json.load(file)

print "LAYER TREE"
print "=========="

print "root"
showGroupItems(root, root["groups"], 1)

# Get layer identifiers only for visible layers
ids = []
for layer in root["wmsLayers"]:
  if layer["visible"]:
    ids.append(layer["id"])

print "\n"
print "MAP LAYER ORDER"
print "==============="
ids.reverse()
for i in range(len(ids)):
  print str(i + 1) + ". " + ids[i]
