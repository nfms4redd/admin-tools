#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import portal

parser = argparse.ArgumentParser(description='Modifica una capa en el fichero layers.json')
parser.add_argument("--file", help="Ruta al fichero layers.json file (por defecto /var/portal/layers.json)", default="/var/portal/layers.json", nargs='?')
parser.add_argument('--id', help="Identificador de la capa a modificar", required=True)
parser.add_argument('--url', help="Nueva URL de la capa de GeoServer")
parser.add_argument('--wmsname', help="Nuevo nombre de la capa en GeoServer")
parser.add_argument('--label', help="Nueva etiqueta de la capa")
parser.add_argument('--start-visible', help="Hace que la capa esté visible al cargar el portal", action="store_true")
parser.add_argument('--start-invisible', help="Hace que la capa esté invisible al cargar el portal", action="store_true")
parser.add_argument('--queryable', help="Hace que la capa se pueda consultar", action="store_true")
parser.add_argument('--not-queryable', help="Hace que la capa no se pueda consultar", action="store_true")
parser.add_argument('--group', help="Identificador del nuevo grupo de la capa")

args = parser.parse_args()
if args.start_visible and args.start_invisible:
  print "No se pueden especificar las opciones --start-visible y --start-invisible a la vez"
  exit(1)
if args.queryable and args.not_queryable:
  print "No se pueden especificar las opciones --queryable y --non-queryable a la vez"
  exit(1)

root = portal.readPortalRoot(args.file)
layerId = args.id
layer = portal.findLayerById(root["portalLayers"], layerId)
wmsLayer = portal.findLayerById(root["wmsLayers"], "wms-" + layerId)

if layer is None or wmsLayer is None:
  print "No se encuentra la capa: " + layerId
  exit(1)

if args.group is not None:
  portal.setLayerInGroup(root, args.group, layerId)

if args.label is not None:
  layer["label"] = args.label

if args.start_visible:
  layer["active"] = True

if args.start_invisible:
  layer["active"] = False

if args.url is not None:
  wmsLayer["baseUrl"] = args.url

if args.wmsname is not None:
  wmsLayer["wmsName"] = args.wmsname

if args.queryable is not None:
  wmsLayer["queryable"] = True

if args.not_queryable is not None:
  wmsLayer["queryable"] = False

portal.writePortalRoot(root, args.file)

