#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import shutil
import os

def getLocalizedDir(layersJson, lang, subDirectory):
  base = os.path.dirname(layersJson)
  directory = os.path.join(base, 'static', 'loc', lang, subDirectory)
  if not os.path.exists(directory):
    os.makedirs(directory)
  return directory

def _updateInlineUrl(portalLayer, mapLayer , url, wmsName):
  portalLayer["inlineLegendUrl"] = (url + "?REQUEST=GetLegendGraphic&" +
            "VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=" +
            wmsName + "&TRANSPARENT=true")

def readPortalRoot(path):
  with open(path, "r") as file:
    return json.load(file)

def writePortalRoot(root, path):
  with open(path, "w") as file:
    json.dump(root, file, indent=4)

def findLayerById(list, id):
  element = None
  for x in list:
    if x.get("id") == id:
      element = x
      break   
  return element

def findGroupById(root, groupId):
  check = lambda currentGroupId, currentGroupItems : groupId == currentGroupId
  rootGroup = { "id": 'root', "items": root["groups"]}
  return findGroupRecursive(rootGroup, check)

def findGroupParent(root, groupId):
  def check(currentGroupId, currentGroupItems):
    for item in currentGroupItems:
      if not isinstance(item, basestring) and item.get("id") == groupId:
        return True
    return False
  rootGroup = { "id": 'root', "items": root["groups"]}
  return findGroupRecursive(rootGroup, check)

def findGroupContainingLayer(root, layerId):
  check = lambda currentGroupId, currentGroupItems : layerId in currentGroupItems
  rootGroup = { "id": 'root', "items": root["groups"]}
  return findGroupRecursive(rootGroup, check)

def findGroupRecursive(currentGroup, check):
  if check(currentGroup.get("id"), currentGroup.get("items")):
    return currentGroup

  for item in currentGroup.get("items"):
    if not isinstance(item, basestring):
      ret = findGroupRecursive(item, check)
      if (ret is not None):
        return ret

  return None

def setLayerInGroup(root, groupId, layerId):
  group = findGroupById(root, groupId)
  if (group is None):
    print "No existe el grupo: " + groupId
  else:
    currentGroup = findGroupContainingLayer(root, layerId)
    if (currentGroup is not None):
      currentGroup.get("items").remove(layerId)
    group.get("items").append(layerId)

def findMapLayers(root, portalLayer):
  ret = []
  mapLayers = root["wmsLayers"]
  for mapLayerId in portalLayer["layers"]:
    ret.append(findLayerById(mapLayers, mapLayerId))
  return ret

def checkMapLayerArgs(args, root):
  if args.queryable and args.not_queryable:
    print "No se pueden especificar las opciones --queryable y --not-queryable a la vez"
    exit(1)
  if args.hidden and args.not_hidden:
    print "No se pueden especificar las opciones --hidden y --not-hidden a la vez"
    exit(1)
  if args.legend:
    if not args.lang:
      print "Es necesario especificar el idioma de la leyenda (--lang)"
      exit(1)
    if not os.path.isfile(args.legend):
      print "El fichero de la leyenda no existe: " + args.legend
      exit(1)

  if args.order is not None:
    nLayers = len(root["wmsLayers"])
    if args.order < 1 or args.order > nLayers:
      print "El orden de la capa no es válido. Debe de estar entre 1 y " + str(nLayers)
      exit(1)

def updateMapLayer(layer, mapLayer, args, root):
  if args.label is not None:
    mapLayer["label"] = args.label

  if args.imageFormat:
    mapLayer["imageFormat"] = args.imageFormat

  if args.sourceLabel:
    mapLayer["sourceLabel"] = args.sourceLabel

  if args.sourceLink:
    mapLayer["sourceLink"] = args.sourceLink

  if args.wmsTime:
    mapLayer["wmsTime"] = args.wmsTime

  if args.wmsName:
    mapLayer["wmsName"] = args.wmsName
    if layer:
      _updateInlineUrl(layer, mapLayer, mapLayer["baseUrl"], args.wmsName)

  if args.url is not None:
    mapLayer["baseUrl"] = args.url
    if layer:
      _updateInlineUrl(layer, mapLayer, args.url, mapLayer["wmsName"])

  if args.queryable:
    mapLayer["queryable"] = True

  if args.not_queryable:
    mapLayer["queryable"] = False

  if args.hidden:
    mapLayer["visible"] = False

  if args.not_hidden:
    mapLayer["visible"] = True

  if args.legend:
    directory = getLocalizedDir(args.file, args.lang, 'images')
    _, extension = os.path.splitext(args.legend)
    filename = mapLayer["id"] + extension
    shutil.copyfile(args.legend, os.path.join(directory, filename))
    mapLayer["legend"] = filename

  if args.order:
    mapLayers = root["wmsLayers"]
    # Since the layers are stored in inverse order we need to transform
    # the index provided by the user (as shown in the portal-layer-tree.py
    # script) to the index in the layer array inside layers.json
    arrayIndex = len(mapLayers) - args.order
    mapLayers.remove(mapLayer)
    mapLayers.insert(arrayIndex, mapLayer)

  return mapLayer

