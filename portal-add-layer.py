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
parser.add_argument('--wmsname', help="Nombre de la capa en GeoServer", required=True)
parser.add_argument('--label', help="Nombre de la nueva capa", required=True)
parser.add_argument('--group', help="Grupo donde se creará la nueva capa", required=True)

args = parser.parse_args()

layerId = args.id
baseUrl = args.url
wmsName = args.wmsname
label = args.label
groupId = args.group

root = portal.readPortalRoot(args.file)

wmsLayerId = "wms-" + layerId

wmsLayer = create(root["wmsLayers"], wmsLayerId)
portalLayer = create(root["portalLayers"], layerId)

wmsLayer["baseUrl"] = baseUrl
wmsLayer["wmsName"] = wmsName
wmsLayer["visible"] = True
wmsLayer["id"] = wmsLayerId

portalLayer["label"] = label
portalLayer["layers"] = [wmsLayerId]
portalLayer["id"] = layerId

portal.setLayerInGroup(root, groupId, layerId)

portal.writePortalRoot(root, args.file)
