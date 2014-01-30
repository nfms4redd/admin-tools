#! /usr/bin/env python

import argparse
import portal

parser = argparse.ArgumentParser(description='Modify layer in layers.json')
parser.add_argument('--id', help="Id of the layer to be modified", required=True)
parser.add_argument('--url', help="Change the url of the WMS server")
parser.add_argument('--wmsname', help="Change the name of the layer in the WMS server")
parser.add_argument('--label', help="Change the name of the layer")
parser.add_argument('--start-visible', help="Make the layer appear visible initially", action="store_true")
parser.add_argument('--start-invisible', help="Make the layer appear invisible initially", action="store_true")
parser.add_argument('--queryable', help="Make the layer queryable", action="store_true")
parser.add_argument('--not-queryable', help="Make the layer not queryable", action="store_true")
parser.add_argument('--group', help="Change the group the layer is in")

args = parser.parse_args()
if args.start_visible and args.start_invisible:
  print "Cannot set both --start-visible and --start-invisible in the same call"
  exit(1)

root = portal.readPortalRoot()
layerId = args.id
layer = portal.findLayerById(root["portalLayers"], layerId)
wmsLayer = portal.findLayerById(root["wmsLayers"], "wms-" + layerId)

if args.group is not None:
  portal.setLayerInGroup(root, args.group, layerId)

if args.label is not None:
  layer["label"] = args.label

if args.start_visible:
  layer["active"] = True

if args.start_invisible:
  layer["active"] = False

if args.url is not None:
  layer["baseUrl"] = args.url

if args.wmsname is not None:
  layer["wmsName"] = args.wmsname

if args.queryable is not None:
  layer["queryable"] = True

if args.not_queryable is not None:
  layer["queryable"] = False

portal.writePortalRoot(root)

