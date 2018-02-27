#!/usr/bin/env python
# # -*- coding: utf-8 -*-
import json
from nfms4redd.Layers import Layers

HELP = 'portal-layers del fichero layers.json'
ADD = 'add'
GET = 'get'
DELETE = 'delete'
UPDATE = 'update'


def add_all_args(parser):
    parser.add_argument('id', help='Identificador de la portal-layer')
    parser.add_argument('-f', '--file', help='Fichero layers.json')
    parser.add_argument('-l', '--label', help='Etiqueta de la portal-layer')
    parser.add_argument(
        '--infoFile',
        help="Fichero HTML con la información de la capa")
    parser.add_argument(
        '--infoLink', help="Enlace con la información de la capa")
    parser.add_argument(
        '--legend',
        dest='inlineLegendUrl',
        help=("URL con una imagen pequeña que situar al lado "
              "del nombre de la capa en el árbol de capas"))
    parser.add_argument(
        '--active',
        dest='active',
        help="Hace que la capa esté visible al cargar el portal",
        action="store_true")
    parser.add_argument(
        '--no-active',
        dest='active',
        help="Hace que la capa esté invisible al cargar el portal",
        action="store_false")
    parser.add_argument(
        '--feedback',
        dest='feedback',
        help="Utilizar la capa para la herramienta feedback",
        action="store_true")
    parser.add_argument(
        '--no-feedback',
        dest='feedback',
        help="No utilizar la capa para la herramienta feedback",
        action="store_false")
    parser.add_argument(
        '--time-instances',
        dest='timeInstances',
        help="Instantes de tiempo en ISO8601 separados por comas")
    parser.add_argument(
        '--time-styles',
        dest='timeStyles',
        help="Nombres de los estilos a utilizar para cada instancia temporal")
    parser.add_argument('--date-format', help="Formato de la fecha")


def configure_parser(parser):
    subparsers = parser.add_subparsers(
        title='Comandos', dest='portal_layers_cmd',
        help='Obtiene información de todas las portal-layers')
    parser.add_argument('-f', '--file', help='Fichero layers.json')

    # Get
    get = subparsers.add_parser(
        GET, help='Obtiene información de una portal-layer')
    get.add_argument('id', help='Identificador de la portal-layer')
    get.add_argument('-f', '--file', help='Fichero layers.json')

    # Add
    add = subparsers.add_parser(ADD, help='Añade una nueva portal-layer')
    add_all_args(add)
    add.add_argument('-g', '--group',
                     help='Grupo que contiene la portal-layer',
                     required=True)

    # Update
    update = subparsers.add_parser(UPDATE, help='Actualiza una portal-layer')
    add_all_args(update)
    update.add_argument('-g', '--group',
                        help='Grupo que contiene la portal-layer')

    # Delete
    delete = subparsers.add_parser(DELETE, help='Elimina una portal-layer')
    delete.add_argument('id', help='Identificador de la portal-layer')
    delete.add_argument('-f', '--file', help='Fichero layers.json')


def show(obj):
    print(json.dumps(obj, indent=4, sort_keys=True))


def run(args):
    layers = Layers(args.file or None)
    if not args.portal_layers_cmd:
        show(layers.portal_layers())
    elif args.portal_layers_cmd == GET:
        portal_layer = layers.portal_layer(args.id)
        if portal_layer is None:
            raise Exception('Invalid portal layer id: ' + args.id)
        show(portal_layer)
    elif args.portal_layers_cmd == ADD:
        del args.portal_layers_cmd
        del args.cmd
        del args.file
        layers.add_portal_layer(args)
        print('Layer has been added.')
    elif args.portal_layers_cmd == UPDATE:
        del args.portal_layers_cmd
        del args.cmd
        del args.file
        layers.update_portal_layer(args)
        print('Layer has been updated.')
    elif args.portal_layers_cmd == DELETE:
        layers.remove_portal_layer(args.id)
        print('Layer has been removed.')
    layers.save()
