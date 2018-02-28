#!/usr/bin/env python
# # -*- coding: utf-8 -*-
from nfms4redd.Layers import Layers
import json

HELP = 'Grupos del fichero layers.json'
ADD = 'add'
GET = 'get'
DELETE = 'delete'
UPDATE = 'update'


def show(obj, out):
    print(json.dumps(obj, indent=4, sort_keys=True), file=out)


def configure_parser(parser):
    subparsers = parser.add_subparsers(
        title='Comandos', dest='groups_cmd',
        help='Obtiene información de todos los grupos')
    parser.add_argument('-f', '--file', help='Fichero layers.json')

    # Get
    get = subparsers.add_parser(GET, help='Obtiene información de un grupo')
    get.add_argument('id', help='Identificador del grupo')
    get.add_argument('-f', '--file', help='Fichero layers.json')

    # Delete
    delete = subparsers.add_parser(DELETE, help='Elimina un grupo')
    delete.add_argument('id', help='Identificador del grupo')
    delete.add_argument('-f', '--file', help='Fichero layers.json')

    # Add
    add = subparsers.add_parser(ADD, help='Añade un nuevo grupo')
    add.add_argument('id', help='Identificador del grupo')
    add.add_argument('-f', '--file', help='Fichero layers.json')
    add.add_argument('-l', '--label', help='Etiqueta del grupo')
    add.add_argument('-p', '--parent',
                     help='Identificador del padre del grupo',
                     required=False)

    # Update
    update = subparsers.add_parser(UPDATE, help='Actualiza un grupo existente')
    update.add_argument('id', help='Identificador del grupo')
    update.add_argument('-f', '--file', help='Fichero layers.json')
    update.add_argument('-l', '--label', help='Etiqueta del grupo')
    update.add_argument('-p', '--parent',
                        help='Identificador del padre del grupo',
                        required=False)


def run(args, layers):
    if not layers:
        layers = Layers(args.file or None)
    if not args.groups_cmd:
        show(layers.groups())
    elif args.groups_cmd == GET:
        group = layers.group(args.id)
        if group is None:
            raise Exception('Invalid group id: ' + args.id)
        show(group)
    elif args.groups_cmd == ADD:
        layers.add_group(args.id, args.label, args.parent)
        show(layers.root['groups'])
    elif args.groups_cmd == DELETE:
        layers.remove_group(args.id)
        print('Group has been removed.')
    elif args.groups_cmd == UPDATE:
        layers.update_group(args.id, args.label, args.parent)
        print('Group has been updated.')
