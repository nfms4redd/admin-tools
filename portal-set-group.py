#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import portal
import json

parser = argparse.ArgumentParser(description='Modifica un grupo en el fichero layers.json')
parser.add_argument("--file", help="Ruta al fichero layers.json file (por defecto /var/portal/layers.json)", default="/var/portal/layers.json", nargs='?')
parser.add_argument('--id', help="Identificador del grupo a modificar", required=True)
parser.add_argument('--label', help="Nueva etiqueta del grupo")
parser.add_argument('--parent', help="Nuevo padre del grupo ('root' para grupo sin padre)")

args = parser.parse_args()

if (args.label is None and args.parent is None):
  print "Se debe especificar uno de los parámetros --label o --parent"
  exit(1)

groupId = args.id
root = portal.readPortalRoot(args.file)
group = portal.findGroupById(root, groupId)

if group is None:
    print "No existe el grupo: " + groupId
    exit(1)

if args.parent is not None:
  newParent = portal.findGroupById(root, args.parent)
  if newParent is None:
    print "No se encuentra el padre: " + args.parent
    exit(1)
  oldParent = portal.findGroupParent(root, groupId)
  if oldParent is not None:
    oldParent["items"].remove(group)
  newParent["items"].append(group)
 
if args.label is not None:
  group["label"] = args.label

portal.writePortalRoot(root, args.file)

