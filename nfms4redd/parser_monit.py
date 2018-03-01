#!/usr/bin/env python
# # -*- coding: utf-8 -*-

import argparse
parser = argparse.ArgumentParser(
    description='Genera configuración de Monit para todas las capas de un '
    'servicio WMS')
parser.add_argument('-u', '--url', required=True, help='URL del servicio WMS')
