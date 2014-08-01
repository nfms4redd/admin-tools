#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import portal
import argparse

parser = argparse.ArgumentParser(description='Elimina una capa de mapa del fichero layers.json')
parser.add_argument("--file", help="Ruta al fichero layers.json file (por defecto /var/portal/layers.json)", default="/var/portal/layers.json", nargs='?')
parser.add_argument('--id', help="Identificador de la capa a eliminar", required=True)
args = parser.parse_args()

args = parser.parse_args()

root = portal.readPortalRoot(args.file)

mapLayer = portal.findLayerById(root["wmsLayers"], args.id)
if not mapLayer:
    print "No se ha podido encontrar la capa de mapa: " + args.id
    exit(1)

portalLayers = root["portalLayers"]

for portalLayer in portalLayers:
  layers = portalLayer["layers"]
  if args.id in layers:
    if len(layers) > 1:
      layers.remove(args.id)
    else:
      print "No se puede eliminar la capa de mapa. La capa de portal '" + portalLayer["id"] + "' no tiene otra capa de mapa asociada."
      exit(1)

root["wmsLayers"].remove(mapLayer)

portal.writePortalRoot(root, args.file)
