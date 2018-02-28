import unittest
import os
import argparse
import json
from nfms4redd.Layers import Layers


class Test(unittest.TestCase):
    def setUp(self):
        self.layers = Layers('test/layers.json')

    def test_root(self):
        with open('test/layers.json', "r") as f:
            self.assertEqual(json.load(f), self.layers.root)

    def test_groups(self):
        groups = self.layers.groups()
        ids = list(map(lambda x: x['id'], groups))
        self.assertEqual(ids, ['base', 'admin', 'landcover', 'emptygroup'])

    def test_get_group(self):
        group = self.layers.group('emptygroup')
        self.assertEqual('emptygroup', group['id'])
        self.assertEqual([], group['items'])

    def test_get_group_recursive(self):
        group = self.layers.group('innerbase')
        self.assertEqual('innerbase', group['id'])
        self.assertEqual(['blue-marble'], group['items'])

    def test_remove_group(self):
        self.layers.remove_group('emptygroup')
        groups = self.layers.groups()
        ids = list(map(lambda x: x['id'], groups))
        self.assertEqual(ids, ['base', 'admin', 'landcover'])

    def test_remove_group_recursive(self):
        self.layers.remove_group('innerbase')
        base = self.layers.group('base')
        items = list(map(lambda x: x['id'], base['items']))
        self.assertEqual(items, ['innerforest'])

    def test_remove_group_invalid(self):
        try:
            self.layers.remove_group('invalid_group')
            self.fail()
        except Exception:
            pass

    def test_add_group(self):
        self.layers.add_group('new_group', label='NEW', parent=None)
        ids = list(map(lambda x: x['id'], self.layers.groups()))
        self.assertEqual('NEW', self.layers.group('new_group')['label'])
        self.assertEqual(ids, ['base', 'admin', 'landcover',
                               'emptygroup', 'new_group'])

    def test_add_group_recursive(self):
        self.layers.add_group('new_group', label='NEW', parent='base')
        base = self.layers.group('base')
        ids = list(map(lambda x: x['id'], base['items']))
        self.assertEqual(ids, ['innerbase', 'innerforest', 'new_group'])

    def test_add_group_invalid_parent(self):
        try:
            self.layers.add_group('new_group', parent='invalid')
            self.fail()
        except Exception:
            pass

    def test_add_group_existing_id(self):
        try:
            self.layers.add_group('base', parent=None)
            self.fail()
        except Exception:
            pass

    def test_portal_layers(self):
        layers = self.layers.portal_layers()
        self.assertEqual(layers, ['blue-marble', 'forestClassification',
                                  'forest_mask', 'countryBoundaries',
                                  'provinces'])

    def test_portal_layer(self):
        layer = self.layers.portal_layer('blue-marble')
        self.assertEqual('blue-marble', layer['id'])
        self.assertEqual(['blue-marble'], layer['layers'])
        self.assertEqual('Blue marble!!!', layer['label'])
        self.assertTrue(layer['active'])

    def test_remove_portal_layer(self):
        self.layers.remove_portal_layer('blue-marble')
        layers = self.layers.portal_layers()
        self.assertEqual(layers, ['forestClassification', 'forest_mask',
                                  'countryBoundaries', 'provinces'])
        self.assertEqual([], self.layers.group('innerbase')['items'])

    def test_remove_portal_layer_invalid(self):
        try:
            self.layers.remove_portal_layer('invalid')
            self.fail()
        except Exception:
            pass

    def test_map_layers(self):
        layers = self.layers.map_layers()
        self.assertEqual(layers, ['blue-marble', 'forestClassification',
                                  'forest_mask', 'countryBoundaries',
                                  'provinces'])

    def test_map_layer(self):
        layer = self.layers.map_layer('blue-marble')
        self.assertEqual('blue-marble', layer['id'])
        self.assertEqual('image/jpeg', layer['imageFormat'])
        self.assertEqual('common:blue_marble', layer['wmsName'])
        self.assertEqual('http://rdc-snsf.org/diss_geoserver/wms',
                         layer['baseUrl'])
        self.assertTrue(layer['visible'])

    def test_remove_map_layer(self):
        self.layers.remove_map_layer('blue-marble')
        layers = self.layers.map_layers()
        self.assertEqual(layers, ['forestClassification', 'forest_mask',
                                  'countryBoundaries', 'provinces'])
        self.assertEqual([], self.layers.portal_layer('blue-marble')['layers'])

    def test_remove_map_layer_invalid(self):
        try:
            self.layers.remove_map_layer('invalid')
            self.fail()
        except Exception:
            pass


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
