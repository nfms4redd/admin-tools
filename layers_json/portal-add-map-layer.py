#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import portal
import argparse

parser = argparse.ArgumentParser(description='Añade una nueva capa de mapa al fichero layers.json')
parser.add_argument("--file", help="Ruta al fichero layers.json file (por defecto /var/portal/layers.json)", default="/var/portal/layers.json", nargs='?')
parser.add_argument('--id', help="Identificador de la nueva capa", required=True)
parser.add_argument('--url', help="URL de la capa de GeoServer", required=True)
parser.add_argument('--wmsName', help="Nombre de la capa en GeoServer", required=True)
parser.add_argument('--label', help="Nombre de la nueva capa", required=True)
parser.add_argument('--portal-layer', help="Capa del portal asociada con esta capa de mapa", required=True)

args = parser.parse_args()

root = portal.readPortalRoot(args.file)

mapLayer = portal.findLayerById(root["wmsLayers"], args.id)
if mapLayer:
    print "Ya existe una capa con ese identificador: " + args.id
    exit(1)

portalLayer = portal.findLayerById(root["portalLayers"], args.portal_layer)
if not portalLayer:
    print "No se ha podido encontrar la capa de portal: " + args.portal_layer
    exit(1)

mapLayer = {}
mapLayer["id"] = args.id
mapLayer["baseUrl"] = args.url
mapLayer["wmsName"] = args.wmsName
mapLayer["label"] = args.label

root["wmsLayers"].append(mapLayer)
portalLayer["layers"].append(args.id)

portal.writePortalRoot(root, args.file)
