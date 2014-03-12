#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import portal 
import argparse

parser = argparse.ArgumentParser(description='Elimina una capa del fichero layers.json')
parser.add_argument("--file", help="Ruta al fichero layers.json file (por defecto /var/portal/layers.json)", default="/var/portal/layers.json", nargs='?')
parser.add_argument('--id', help="Identificador de la capa a eliminar", required=True)
args = parser.parse_args()

root = portal.readPortalRoot(args.file)
portalLayer = portal.findLayerById(root["portalLayers"], args.id)

if not portalLayer:
  print "No existe la capa: " + args.id
  exit(1)

mapLayers = portal.findMapLayers(root, portalLayer)
for layer in mapLayers:
  root["wmsLayers"].remove(layer);
root["portalLayers"].remove(portalLayer);

group = portal.findGroupContainingLayer(root, args.id)
if group:
  group.get("items").remove(args.id)

portal.writePortalRoot(root, args.file)
