#!/usr/bin/env python
# # -*- coding: utf-8 -*-
from nfms4redd.Layers import Layers
import json

HELP = 'Árbol de capas del fichero layers.json'


def show(obj):
    print(json.dumps(obj, indent=4, sort_keys=True))


def configure_parser(parser):
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
    print("LAYER TREE")
    print("==========")
    print("/")
    _showGroupItems(root["groups"], 1)

    # Get layer identifiers only for visible layers
    ids = []
    for layer in root["wmsLayers"]:
        if layer["visible"]:
            ids.append(layer["id"])

    print("\n")
    print("MAP LAYER ORDER")
    print("===============")
    ids.reverse()
    for i in range(len(ids)):
        print(str(i + 1) + ". " + ids[i])
