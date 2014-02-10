#! /usr/bin/env python

import argparse
import portal
import json

parser = argparse.ArgumentParser(description='Manage groups in layers.json')
parser.add_argument("--file", help="Path to the layers.json file (default /var/portal/layers.json)", default="/var/portal/layers.json", nargs='?')
parser.add_argument('--id', help="Id of the group to manage", required=True)
parser.add_argument('--label', help="Change the label of the group")
parser.add_argument('--parent', help="Change the parent of the group (root for no parent)")

args = parser.parse_args()

if (args.label is None and args.parent is None):
  print "Either --label or --parent has to be specified"
  exit(1)

groupId = args.id
root = portal.readPortalRoot(args.file)
group = portal.findGroupById(root, groupId)

if group is None:
    print "No such group: " + groupId
    exit(1)

if args.parent is not None:
  newParent = portal.findGroupById(root, args.parent)
  if newParent is None:
    print "Cannot find the group: " + args.parent
    exit(1)
  oldParent = portal.findGroupParent(root, groupId)
  if oldParent is not None:
    oldParent["items"].remove(group)
  newParent["items"].append(group)
 
if args.label is not None:
  group["label"] = args.label

portal.writePortalRoot(root, args.file)

