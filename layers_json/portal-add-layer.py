#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import portal
import argparse

def create(list, id):
  ret = portal.findLayerById(list, id)

  if ret is not None:
    print "Ya existe una capa con ese identificador: " + layerId
    exit(1)

  ret = {}
  list.append(ret)
  return ret

parser = argparse.ArgumentParser(description='Añade una nueva capa al fichero layers.json')
parser.add_argument("--file", help="Ruta al fichero layers.json file (por defecto /var/portal/layers.json)", default="/var/portal/layers.json", nargs='?')
parser.add_argument('--id', help="Identificador de la nueva capa", required=True)
parser.add_argument('--url', help="URL de la capa de GeoServer", required=True)
parser.add_argument('--wmsName', help="Nombre de la capa en GeoServer", required=True)
parser.add_argument('--label', help="Nombre de la nueva capa", required=True)
parser.add_argument('--group', help="Grupo donde se creará la nueva capa", required=True)

args = parser.parse_args()

root = portal.readPortalRoot(args.file)

if not portal.findGroupById(root, args.group):
  print "No se ha encontrado el grupo: " + args.group
  exit(1)

mapLayerId = "map-" + args.id
mapLayer = create(root["wmsLayers"], mapLayerId)
portalLayer = create(root["portalLayers"], args.id)

mapLayer["baseUrl"] = args.url
mapLayer["wmsName"] = args.wmsName
mapLayer["visible"] = True
mapLayer["label"] = args.label
mapLayer["id"] = mapLayerId

portalLayer["label"] = args.label
portalLayer["layers"] = [mapLayerId]
portalLayer["id"] = args.id

portal.setLayerInGroup(root, args.group, args.id)

portal.writePortalRoot(root, args.file)
