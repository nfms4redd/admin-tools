#! /usr/bin/env python

import json
import argparse

def showGroupItems(items, indent):
  for item in items:
    if isinstance(item, basestring):
      print('\t' * indent + item)
    else:
      print('\t' * indent + item.get("id"))
      showGroupItems(item.get("items"), indent+1)

parser=argparse.ArgumentParser(description='''Shows the layer tree as specified in layers.json.''', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--file", help="Path to the layers.json file", default="/var/layers.json", nargs='?')
args=parser.parse_args()

with open(args.file, "r") as file:
  root=json.load(file)

print "root"
showGroupItems(root["groups"], 1)

