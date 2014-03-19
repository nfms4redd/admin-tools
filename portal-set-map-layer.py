#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import portal

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
parser.add_argument('--lang', help="Idioma de la leyenda o fichero de información que se quiere modificar.")
parser.add_argument('--queryable', help="Hace que la capa se pueda consultar", action="store_true")
parser.add_argument('--not-queryable', help="Hace que la capa no se pueda consultar", action="store_true")
parser.add_argument('--hidden', help="Hace que la capa no se muestre nunca ni en el mapa ni en el árbol de capas", action="store_true")
parser.add_argument('--not-hidden', help="Hace que la capa se pueda mostrar y ocultar", action="store_true")
parser.add_argument('--order', help="Orden de la capa para el dibujado", type=int)

args = parser.parse_args()

root = portal.readPortalRoot(args.file)

portal.checkMapLayerArgs(args, root)

mapLayer = portal.findLayerById(root["wmsLayers"], args.id)

if mapLayer is None:
  print "No se encuentra la capa: " + args.id
  exit(1)

#Find portal layer
portalLayer = None
for layer in root["portalLayers"]:
  if args.id in layer["layers"]:
    portalLayer = layer
    break

mapLayer = portal.updateMapLayer(portalLayer, mapLayer, args, root)
portal.writePortalRoot(root, args.file)

