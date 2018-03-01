#!/usr/bin/env python
# # -*- coding: utf-8 -*-

import argparse
from nfms4redd import groups, portal_layers, map_layers, tree


actions = {
    'groups': groups,
    'portal-layers': portal_layers,
    'map-layers': map_layers,
    'tree': tree
}

parser = argparse.ArgumentParser(
    description='Línea de comandos para manejar el fichero layers.json')

subparsers = parser.add_subparsers(title='Comandos', dest='cmd')

for key in actions:
    subparser = subparsers.add_parser(key, help=actions[key].HELP)
    actions[key].configure_parser(subparser)
