import json

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

