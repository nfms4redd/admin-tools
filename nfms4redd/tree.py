#!/usr/bin/env python
# # -*- coding: utf-8 -*-
from nfms4redd.Layers import Layers
import json

HELP = 'Muestra el árbol de capas y el orden de dibujado'


def show(obj):
    print(json.dumps(obj, indent=4, sort_keys=True))


def configure_parser(parser):
    parser.description = HELP
    parser.add_argument('-f', '--file', help='Fichero layers.json')


def run(args):
    layers = Layers(args.file)
    root = layers.root

    def _showGroupItems(items, indent):
        for item in items:
            if isinstance(item, str):
                portalLayer = layers.portal_layer(item)
                if portalLayer:
                    mapLayers = portalLayer["layers"]
                    print('\t' * indent + item +
                          " (" + ", ".join(mapLayers) + ")")
            else:
                print('\t' * indent + item.get("id"))
                _showGroupItems(item.get("items"), indent + 1)
    print("ÁRBOL")
    print("=====")
    print("/")
    _showGroupItems(root["groups"], 1)

    # Get layer identifiers only for visible layers
    ids = []
    for layer in root["wmsLayers"]:
        if layer["visible"]:
            ids.append(layer["id"])

    print("\n")
    print("ORDER DE DIBUJADO")
    print("=================")
    ids.reverse()
    for i in range(len(ids)):
        print(str(i + 1) + ". " + ids[i])
