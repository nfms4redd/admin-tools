#! /usr/bin/env python

import json

def showGroupItems(items, indent):
  for item in items:
    if isinstance(item, basestring):
      print('\t' * indent + item)
    else:
      print('\t' * indent + item.get("id"))
      showGroupItems(item.get("items"), indent+1)

with open("layers.json", "r") as file:
  root=json.load(file)

print "root"
showGroupItems(root["groups"], 1)

