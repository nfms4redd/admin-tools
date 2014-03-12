#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import portal
import os
import shutil

parser = argparse.ArgumentParser(description='Modifica una capa en el fichero layers.json')
parser.add_argument("--file", help="Ruta al fichero layers.json file (por defecto /var/portal/layers.json)", default="/var/portal/layers.json", nargs='?')
parser.add_argument('--id', help="Identificador de la capa a modificar", required=True)
parser.add_argument('--url', help="Nueva URL de la capa de GeoServer")
parser.add_argument('--wmsName', help="Nuevo nombre de la capa en GeoServer")
parser.add_argument('--wmsTime', help="Cadena que contiene los diferentes instantes temporales que se pueden pedir a GeoServer")
parser.add_argument('--imageFormat', help="Formato de la imagen que se pedirá a GeoServer")
parser.add_argument('--sourceLabel', help="Etiqueta de la fuente de datos")
parser.add_argument('--sourceLink', help="Enlace informativo a la fuente de datos")
parser.add_argument('--label', help="Nueva etiqueta de la capa")
parser.add_argument('--legend', help="Imagen que contiene la leyenda de la capa. Es necesario especificar el idioma de la leyenda (--lang)")
parser.add_argument('--infoFile', help="Fichero HTML con la información de la capa. Es necesario especificar el idioma de la leyenda (--lang)")
parser.add_argument('--lang', help="Idioma de la leyenda o fichero de información que se quiere modificar.")
parser.add_argument('--start-visible', help="Hace que la capa esté visible al cargar el portal", action="store_true")
parser.add_argument('--start-invisible', help="Hace que la capa esté invisible al cargar el portal", action="store_true")
parser.add_argument('--queryable', help="Hace que la capa se pueda consultar", action="store_true")
parser.add_argument('--not-queryable', help="Hace que la capa no se pueda consultar", action="store_true")
parser.add_argument('--hidden', help="Hace que la capa no se muestre nunca ni en el mapa ni en el árbol de capas", action="store_true")
parser.add_argument('--not-hidden', help="Hace que la capa se pueda mostrar y ocultar", action="store_true")
parser.add_argument('--group', help="Identificador del nuevo grupo de la capa")

args = parser.parse_args()

# Check arguments
if args.start_visible and args.start_invisible:
  print "No se pueden especificar las opciones --start-visible y --start-invisible a la vez"
  exit(1)
if args.infoFile:
  if not args.lang:
    print "Es necesario especificar el idioma del fichero de información (--lang)"
    exit(1)
  if not os.path.isfile(args.infoFile):
    print "El fichero de información no existe: " + args.legend
    exit(1)
portal.checkMapLayerArgs(args)

# Get layer and mapLayer
root = portal.readPortalRoot(args.file)
layerId = args.id
layer = portal.findLayerById(root["portalLayers"], layerId)

if layer is None:
  print "No se encuentra la capa: " + layerId
  exit(1)

mapLayers = portal.findMapLayers(root, layer)

# Check mapLayer options
if len(mapLayers) != 1:
  if (args.url or args.wmsname or args.queryable or args.not_queryable or
      args.hidden or args.not_hidden or args.imageFormat or sourceLabel or
      args.sourceLink or args.legend or args.wmsTime or args.legend):
    print ("Error!!")
    exit(1)
  mapLayer = None
else:
  mapLayer = mapLayers[0]

if args.group:
  portal.setLayerInGroup(root, args.group, layerId)

if args.label:
  layer["label"] = args.label

if args.start_visible:
  layer["active"] = True

if args.start_invisible:
  layer["active"] = False

if args.infoFile:
  directory = portal.getLocalizedDir(args.file, args.lang, 'html')
  filename = args.id + ".html"
  shutil.copyfile(args.infoFile, os.path.join(directory, filename))
  layer["infoFile"] = filename

if mapLayer:
  mapLayer = portal.updateMapLayer(layer, mapLayer, args)

portal.writePortalRoot(root, args.file)

