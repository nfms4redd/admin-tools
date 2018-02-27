#!/usr/bin/env python
# # -*- coding: utf-8 -*-
import json
from nfms4redd.Layers import Layers
HELP = 'map-layers del fichero layers.json'
ADD = 'add'
GET = 'get'
DELETE = 'delete'
UPDATE = 'update'


def _add_all_arguments(parser, creating):
    parser.add_argument('id', help='Identificador de la map-layer')
    parser.add_argument('-f', '--file', help='Fichero layers.json')
    parser.add_argument(
        '-t', '--type',
        choices=['wms', 'osm', 'gmaps'],
        help="Tipo de capa",
        required=creating)
    parser.add_argument('-p', '--portal-layer',
                        help='Portal-layer que contiene la map-layer',
                        required=creating)
    parser.add_argument(
        '--legend',
        help="Nombre del fichero imagen con la leyenda de la capa")
    parser.add_argument(
        '--sourceLink', help="URL del proveedor de los datos")
    parser.add_argument(
        '--sourceLabel',
        help="Texto con el que presentar el enlace especificado en sourceLink")
    parser.add_argument(
        '-l', '--label', help="Etiqueta de la capa")
    parser.add_argument(
        '-u', '--url', nargs='*',
        help="URL del servicio de la capa (WMS o OSM)")
    parser.add_argument(
        '--visible', dest='visible', action='store_const', const=True,
        help="URL del servicio de la capa (WMS o OSM)")
    parser.add_argument(
        '--no-visible', dest='visible', action='store_const', const=False,
        help="URL del servicio de la capa (WMS o OSM)")
    if not creating:
        parser.add_argument(
            '--order', type=int,
            help="Orden de la capa en el mapa")

    # gmaps
    parser.add_argument(
        '--gmaps-type',
        choices=["ROADMAP", "SATELLITE", "HYBRID", "TERRAIN"],
        help="Tipo de capa Google")

    # wms
    parser.add_argument('-n', '--wmsName',
                        help="Nombre de la capa en el servicio WMS")
    parser.add_argument(
        '--imageFormat',
        help="Formato de imagen a utilizar en las llamadas WMS")
    parser.add_argument(
        '--queryType', choices=['wms', 'wfs'],
        help="Protocolo usado para la herramienta de información")
    parser.add_argument(
        '--queryUrl',
        help="URL base a utilizar en la petición de información")
    parser.add_argument(
        '--queryGeomFieldName',
        help="El nombre del campo geométrico (solo para wfs)")
    parser.add_argument(
        '--queryFieldNames', choices=['wms', 'wfs'],
        help="Nombres de los campos que se quieren obtener (solo para wfs)")
    parser.add_argument(
        '--queryFieldAliases', choices=['wms', 'wfs'],
        help="Aliases de los campos especificados en queryFieldNames")
    parser.add_argument(
        '--queryTimeFieldName',
        help="Nombre del campo temporal (solo para wfs)")
    parser.add_argument(
        '--queryHighlightBounds',
        dest="queryHighlightBounds",
        action="store_const", const=True,
        help="Resalta únicamente el rectángulo de encuadre (solo para wms)")
    parser.add_argument(
        '--no-queryHighlightBounds',
        dest="queryHighlightBounds",
        action="store_const", const=False,
        help="Resalta toda la geometría (solo para wms)")


def configure_parser(parser):
    subparsers = parser.add_subparsers(
        title='Comandos', dest='map_layers_cmd',
        help='Obtiene información de todas las map-layers')
    parser.add_argument('-f', '--file', help='Fichero layers.json')

    # Get
    get = subparsers.add_parser(
        GET, help='Obtiene información de una map-layer')
    get.add_argument('id', help='Identificador de la map-layer')
    get.add_argument('-f', '--file', help='Fichero layers.json')

    # Delete
    delete = subparsers.add_parser(DELETE, help='Elimina una map-layer')
    delete.add_argument('id', help='Identificador de la map-layer')
    delete.add_argument('-f', '--file', help='Fichero layers.json')

    # Add
    add = subparsers.add_parser(ADD, help='Añade una nueva map-layer')
    _add_all_arguments(add, True)

    # Update
    update = subparsers.add_parser(
        UPDATE, help='Actualiza una map-layer existente')
    _add_all_arguments(update, False)


def show(obj):
    print(json.dumps(obj, indent=4, sort_keys=True))


def run(args):
    layers = Layers(args.file or None)
    if not args.map_layers_cmd:
        show(layers.map_layers())
    elif args.map_layers_cmd == GET:
        layer = layers.map_layer(args.id)
        if layer is None:
            raise Exception('Invalid map layer id: ' + args.id)
        show(layer)
    elif args.map_layers_cmd == ADD:
        del args.map_layers_cmd
        del args.cmd
        del args.file
        layers.add_map_layer(args)
        print('Layer has been added.')
    elif args.map_layers_cmd == UPDATE:
        del args.map_layers_cmd
        del args.cmd
        del args.file
        layers.update_map_layer(args)
        print('Layer has been updated.')
    elif args.map_layers_cmd == DELETE:
        layers.remove_map_layer(args.id)
        print('Layer has been removed.')
    layers.save()
