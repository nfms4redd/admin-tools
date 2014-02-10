#! /usr/bin/env python

import argparse
import portal
import json

parser = argparse.ArgumentParser(description='Manage groups in layers.json')
parser.add_argument("--file", help="Path to the layers.json file (default /var/portal/layers.json)", default="/var/portal/layers.json", nargs='?')
parser.add_argument('--id', help="Id of the group to manage", required=True)
parser.add_argument('--label', help="Change the label of the group", required=True)
parser.add_argument('--parent', help="Change the parent of the group (root for no parent)", required=True)

args = parser.parse_args()

root = portal.readPortalRoot(args.file)

if portal.findGroupById(root, args.id) is not None:
    print "Group already exists: " + args.id
    exit(1)

newParent = portal.findGroupById(root, args.parent)

if newParent is None:
  print "Cannot find the group: " + args.parent
  exit(1)

group = { "id": args.id, "label": args.label, "items":[]}

oldParent = portal.findGroupParent(root, args.id)
if oldParent is not None:
  oldParent["items"].remove(group)

newParent["items"].append(group)
 
portal.writePortalRoot(root, args.file)

