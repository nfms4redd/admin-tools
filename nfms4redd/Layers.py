#!/usr/bin/env python
# # -*- coding: utf-8 -*-
import json
import os


class Layers:
    def __init__(self, f):
        if not f:
            f = os.environ.get('GEOLADRIS_LAYERS_JSON')

        if not f:
            raise Exception('Se debe especificar el fichero layers.json'
                            '(-f/--file o variable de entorno '
                            'GEOLADRIS_LAYERS_JSON)')
        if not os.path.isfile(f):
            raise Exception('El fichero layers.json no es válido: ' + f)

        self.path = f
        self.reload()

    def reload(self):
        with open(self.path, "r") as f:
            self.root = json.load(f)

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.root, f, indent=4, sort_keys=True)

    def root(self):
        return self.root

    def groups(self):
        return self.root['groups']

    def group(self, id):
        return self._find_group_recursive(
            {'items': self.root['groups']},
            lambda x: x == id or ('id' in x and x['id'] == id))

    def portal_layers(self):
        return list(map(lambda x: x['id'], self.root['portalLayers']))

    def portal_layer(self, id):
        layer = [l for l in self.root['portalLayers'] if l['id'] == id]
        return layer[0] if len(layer) == 1 else None

    def _find_group_recursive(self, currentGroup, testFunction):
        if testFunction(currentGroup):
            return currentGroup
        elif 'items' not in currentGroup:
            return False
        for item in currentGroup['items']:
            if not isinstance(item, str):
                ret = self._find_group_recursive(item, testFunction)
                if ret is not None:
                    return ret
        return None

    def _find_group_parent(self, id):
        def check(currentGroup):
            if 'items' not in currentGroup:
                return None
            for item in currentGroup['items']:
                if ((isinstance(item, str) and item == id) or
                        (not isinstance(item, str) and item['id'] == id)):
                    return True
            return False

        return self._find_group_recursive({
            'items': self.root['groups']
        }, check)

    def add_group(self, id, label=None, parent=None):
        if self.group(id):
            raise Exception('Group id already exists: ' + id)

        if parent:
            parentGroup = self.group(parent)
            if not parentGroup:
                raise Exception('Invalid parent id: ' + parent)
            parentItems = parentGroup['items']
        else:
            parentItems = self.root['groups']

        parentItems.append({
            'id': id,
            'label': label or id,
            'items': []
        })

    def remove_group(self, id):
        group = self.group(id)
        parent = self._find_group_parent(id)

        if not group:
            raise Exception('Cannot find group for id: ' + id)
        if not parent:
            raise Exception('Cannot find parent for group with id: ' + id)

        parent['items'].remove(group)

    def update_group(self, id, label, parent):
        group = self.group(id)
        oldParent = self._find_group_parent(id)

        if not group:
            raise Exception('Cannot find group for id: ' + id)

        if label:
            group['label'] = label

        if parent and parent != oldParent['id']:
            newParent = self.group(parent)
            if not newParent:
                raise Exception('Cannot find new parent: ' + parent)
            newParent['items'].append(group)
            oldParent['items'].remove(group)

    def add_portal_layer(self, args):
        portal_layer = self.portal_layer(args.id)
        if portal_layer:
            raise Exception('Portal-layer id already exists: ' + args.id)

        group = self.group(args.group)
        if not group:
            raise Exception('Cannot find group for id: ' + args.group)

        portal_layer = {k: v for k, v in vars(args).items() if v is not None}
        portal_layer['layers'] = []
        del portal_layer['group']

        group['items'].append(args.id)
        self.root['portalLayers'].append(portal_layer)

    def update_portal_layer(self, args):
        portal_layer = self.portal_layer(args.id)
        if not portal_layer:
            raise Exception('Cannot find portal-layer for id: ' + args.id)

        if args.group:
            new_group = self.group(args.group)
            if not new_group:
                raise Exception('Cannot find group for id: ' + args.group)

        new_portal_layer = {k: v for k, v in vars(args).items()
                            if v is not None}
        portal_layer.update(new_portal_layer)
        del portal_layer['group']

        old_group = self._find_group_parent(args.id)
        if new_group and new_group['id'] != old_group['id']:
            new_group['items'].append(args.id)
            old_group['items'].remove(args.id)

    def remove_portal_layer(self, id):
        portal_layer = self.portal_layer(id)
        parent = self._find_group_parent(id)

        if not portal_layer:
            raise Exception('Cannot find portal layer for id: ' + id)
        if not parent:
            raise Exception('Cannot find parent for group with id: ' + id)

        self.root['portalLayers'].remove(portal_layer)
        parent['items'].remove(portal_layer['id'])
