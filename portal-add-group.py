#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import portal
import json

parser = argparse.ArgumentParser(description='Añade un nuevo grupo al fichero layers.json')
parser.add_argument("--file", help="Ruta al fichero layers.json file (por defecto /var/portal/layers.json)", default="/var/portal/layers.json", nargs='?')
parser.add_argument('--id', help="Identificador del nuevo grupo", required=True)
parser.add_argument('--label', help="Etiqueta del nuevo grupo", required=True)
parser.add_argument('--parent', help="Identificador del grupo padre ('root' para añadir grupo sin padre)", required=True)

args = parser.parse_args()

root = portal.readPortalRoot(args.file)

if portal.findGroupById(root, args.id) is not None:
    print "El grupo ya existe: " + args.id
    exit(1)

newParent = portal.findGroupById(root, args.parent)

if newParent is None:
  print "No se ha podido encontrar el padre: " + args.parent
  exit(1)

group = { "id": args.id, "label": args.label, "items":[]}

oldParent = portal.findGroupParent(root, args.id)
if oldParent is not None:
  oldParent["items"].remove(group)

newParent["items"].append(group)
 
portal.writePortalRoot(root, args.file)

