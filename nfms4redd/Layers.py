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

    def map_layers(self):
        return list(map(lambda x: x['id'], self.root['wmsLayers']))

    def map_layer(self, id):
        layer = [l for l in self.root['wmsLayers'] if l['id'] == id]
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

    def _find_map_layer_parent(self, id):
        layers = list(filter(lambda x: id in x['layers'],
                             self.root['portalLayers']))
        return layers[0] if len(layers) == 1 else None

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

        new_group = None
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

    def _map_layer_from_args(self, args):
        if args.type == 'wms':
            layer = vars(args)
            if layer['url']:
                layer['baseUrl'] = layer['url'][0]
            layer['url'] = layer['gmaps_type'] = layer['portal_layer'] = \
                layer['order'] = None
        elif args.type == 'osm':
            layer = {'osmUrls': args.url}
        elif args.type == 'gmaps':
            layer = {'gmaps-type': args.gmaps_type}

        baseProps = {
            'id': args.id,
            'type': args.type,
            'sourceLink': args.sourceLink,
            'sourceLabel': args.sourceLabel,
            'legend': args.legend,
            'label': args.label
        }

        layer.update(baseProps)
        return {k: v for k, v in layer.items() if v is not None}

    def add_map_layer(self, args):
        if args.type in ['wms', 'osm'] and not args.url:
            raise Exception('--url is mandatory for type ' + args.type)
        elif args.type == 'gmaps' and not args.gmaps_type:
            raise Exception('--gmaps-type is mandatory for type ' + args.type)
        elif args.type == 'wms' and not args.wmsName:
            raise Exception('--wmsName is mandatory for type ' + args.type)
        elif self.map_layer(args.id):
            raise Exception('Map-layer id already exists: ' + args.id)

        portal_layer = self.portal_layer(args.portal_layer)
        if not portal_layer:
            raise Exception('Cannot find portal-layer for id: '
                            + args.portal_layer)

        layer = self._map_layer_from_args(args)

        portal_layer['layers'].append(args.id)
        self.root['wmsLayers'].append(layer)

    def update_map_layer(self, args):
        layer = self.map_layer(args.id)
        if not layer:
            raise Exception('Cannot find map-layer for id: ' + args.id)

        new_portal_layer = None
        if args.portal_layer:
            new_portal_layer = self.portal_layer(args.portal_layer)
            if not new_portal_layer:
                raise Exception('Cannot find group for id: '
                                + args.portal_layer)

        if args.order is not None:
            nLayers = len(self.root["wmsLayers"])
            if args.order < 1 or args.order > nLayers:
                raise Exception("El orden de la capa no es válido. "
                                "Debe de estar entre 1 y " + str(nLayers))
            layers = self.root["wmsLayers"]
            # Since the layers are stored in inverse order we need to transform
            # the index provided by the user to the index in the layer array
            # inside layers.json
            index = len(layers) - args.order
            layers.remove(layer)
            layers.insert(index, layer)

        if not args.type:
            args.type = layer['type'] if 'type' in layer else 'wms'
        new_layer = self._map_layer_from_args(args)
        layer.update(new_layer)

        old_portal_layer = self._find_map_layer_parent(args.id)
        if (new_portal_layer and
                new_portal_layer['id'] != old_portal_layer['id']):
            new_portal_layer['layers'].append(args.id)
            old_portal_layer['layers'].remove(args.id)

    def remove_map_layer(self, id):
        layer = self.map_layer(id)
        parent = self._find_map_layer_parent(id)

        if not layer:
            raise Exception('Cannot find portal layer for id: ' + id)
        if not parent:
            raise Exception('Cannot find parent for group with id: ' + id)

        self.root['wmsLayers'].remove(layer)
        parent['layers'].remove(layer['id'])
