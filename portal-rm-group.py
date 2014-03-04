#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import portal 
import argparse

parser = argparse.ArgumentParser(description='Elimina un grupo del fichero layers.json')
parser.add_argument("--file", help="Ruta al fichero layers.json file (por defecto /var/portal/layers.json)", default="/var/portal/layers.json", nargs='?')
parser.add_argument('--id', help="Identificador del grupo a eliminar", required=True)
args = parser.parse_args()

root = portal.readPortalRoot(args.file)
group = portal.findGroupById(root, args.id)
parent = portal.findGroupParent(root, args.id)

if not group:
  print "No se ha podido encontrar el grupo: " + args.id
  exit(1)

parent.get("items").remove(group)

portal.writePortalRoot(root, args.file)
