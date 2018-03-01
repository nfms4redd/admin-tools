import unittest
import os
import argparse
import json
from nfms4redd.Layers import Layers


class Test(unittest.TestCase):
    def setUp(self):
        self.layers = Layers('test/layers.json')

    def _emtpy_map_layer_args(self, id=None, type=None):
        args = argparse.Namespace(id=id, type=type)
        args.wmsName = None
        args.legend = None
        args.sourceLink = None
        args.sourceLabel = None
        args.label = None
        args.url = None
        args.visible = None
        args.order = None
        args.portal_layer = None
        args.gmaps_type = None
        args.imageFormat = None
        args.queryType = None
        args.queryUrl = None
        args.queryGeomFieldName = None
        args.queryFieldNames = None
        args.queryFieldAliases = None
        args.queryTimeFieldName = None
        args.queryHighlightBounds = None
        return args

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

    def test_update_group(self):
        self.layers.update_group('base', 'NEW LABEL', None)
        self.assertEqual('NEW LABEL', self.layers.group('base')['label'])

    def test_update_group_new_parent(self):
        self.layers.update_group('admin', None, 'base')
        items = self.layers.group('base')['items']
        self.assertTrue('admin' in list(map(lambda x: x['id'], items)))

    def test_update_group_invalid_id(self):
        try:
            self.layers.update_group('invalid', None, None)
            self.fail()
        except Exception as e:
            pass

    def test_update_group_invalid_parent(self):
        try:
            self.layers.update_group('innerbase', None, 'invalid')
            self.fail()
        except Exception as e:
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

    def test_add_portal_layer(self):
        args = argparse.Namespace()
        args.id = 'new_group'
        args.group = 'innerbase'
        args.active = True
        args.feedback = None
        self.layers.add_portal_layer(args)
        layer = self.layers.portal_layer(args.id)
        self.assertTrue(layer['active'])
        self.assertTrue('feedback' not in layer)

    def test_add_portal_layer_invalid_parent(self):
        args = argparse.Namespace()
        args.id = 'new_layer'
        args.group = 'invalid'
        try:
            self.layers.add_portal_layer(args)
            self.fail()
        except Exception as e:
            pass

    def test_add_portal_layer_existing_id(self):
        args = argparse.Namespace()
        args.id = 'blue-marble'
        args.group = 'innerbase'
        try:
            self.layers.add_portal_layer(args)
            self.fail()
        except Exception as e:
            pass

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

    def test_update_portal_layer(self):
        args = argparse.Namespace(id='blue-marble', group=None, feedback=True)
        self.layers.update_portal_layer(args)
        self.assertTrue(self.layers.portal_layer('blue-marble')['feedback'])

    def test_update_portal_layer_new_parent(self):
        args = argparse.Namespace(id='blue-marble', group='admin')
        self.layers.update_portal_layer(args)
        self.assertTrue('blue-marble' in self.layers.group('admin')['items'])
        self.assertFalse(
            'blue-marble' in self.layers.group('innerbase')['items'])

    def test_update_portal_layer_invalid_id(self):
        args = argparse.Namespace(id='invalid')
        try:
            self.layers.update_portal_layer(args)
            self.fail()
        except Exception as e:
            pass

    def test_update_portal_layer_invalid_parent(self):
        args = argparse.Namespace(id='blue-marble', group='invalid')
        try:
            self.layers.update_portal_layer(args)
            self.fail()
        except Exception as e:
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

    def test_add_map_layer_wms(self):
        args = self._emtpy_map_layer_args('new_layer', 'wms')
        args.portal_layer = 'blue-marble'
        args.url = 'http://localhost:8080/geoserver/wms'
        args.wmsName = 'mylayer'
        self.layers.add_map_layer(args)
        layer = self.layers.map_layer(args.id)
        self.assertEqual({
            'baseUrl': 'http://localhost:8080/geoserver/wms',
            'id': 'new_layer',
            'type': 'wms',
            'wmsName': 'mylayer'
        }, layer)
        portal_layer = self.layers.portal_layer('blue-marble')
        self.assertTrue('new_layer' in portal_layer['layers'])

    def test_add_map_layer_osm(self):
        args = self._emtpy_map_layer_args('new_layer', 'osm')
        args.portal_layer = 'blue-marble'
        args.url = ['http://localhost:8080/geoserver/wms']
        self.layers.add_map_layer(args)
        layer = self.layers.map_layer(args.id)
        self.assertEqual({
            'osmUrls': ['http://localhost:8080/geoserver/wms'],
            'id': 'new_layer',
            'type': 'osm'
        }, layer)
        portal_layer = self.layers.portal_layer('blue-marble')
        self.assertTrue('new_layer' in portal_layer['layers'])

    def test_add_map_layer_gmaps(self):
        args = self._emtpy_map_layer_args('new_layer', 'gmaps')
        args.portal_layer = 'blue-marble'
        args.gmaps_type = 'ROADMAP'
        self.layers.add_map_layer(args)
        layer = self.layers.map_layer(args.id)
        self.assertEqual({
            'id': 'new_layer',
            'gmaps-type': 'ROADMAP',
            'type': 'gmaps'
        }, layer)
        portal_layer = self.layers.portal_layer('blue-marble')
        self.assertTrue('new_layer' in portal_layer['layers'])

    def test_add_map_layer_missing_url(self):
        args = self._emtpy_map_layer_args('new_layer', 'wms')
        args.portal_layer = 'blue-marble'
        args.wmsName = 'mylayer'
        try:
            self.layers.add_map_layer(args)
            self.fail()
        except Exception as e:
            pass

    def test_add_map_layer_missing_wmsname(self):
        args = self._emtpy_map_layer_args('new_layer', 'wms')
        args.portal_layer = 'blue-marble'
        args.url = 'http://localhost:8080/geoserver/wms'
        try:
            self.layers.add_map_layer(args)
            self.fail()
        except Exception as e:
            pass

    def test_add_map_layer_missing_gmaps_type(self):
        args = self._emtpy_map_layer_args('new_layer', 'gmaps')
        try:
            self.layers.add_map_layer(args)
            self.fail()
        except Exception as e:
            pass

    def test_add_map_layer_invalid_parent(self):
        args = self._emtpy_map_layer_args('new_layer', 'wms')
        args.portal_layer = 'invalid'
        args.wmsName = 'mylayer'
        args.url = 'http://localhost:8080/geoserver/wms'
        try:
            self.layers.add_map_layer(args)
            self.fail()
        except Exception as e:
            pass

    def test_add_map_layer_existing_id(self):
        args = self._emtpy_map_layer_args('blue-marble', 'wms')
        args.portal_layer = 'blue-marble'
        args.wmsName = 'mylayer'
        args.url = 'http://localhost:8080/geoserver/wms'
        try:
            self.layers.add_map_layer(args)
            self.fail()
        except Exception as e:
            pass

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

    def test_update_map_layer(self):
        args = self._emtpy_map_layer_args('blue-marble')
        args.visible = True
        self.layers.update_map_layer(args)
        self.assertTrue(self.layers.map_layer('blue-marble')['visible'])

    def test_update_portal_layer_new_parent(self):
        args = self._emtpy_map_layer_args('blue-marble')
        args.portal_layer = 'provinces'
        self.layers.update_map_layer(args)
        layers = self.layers.portal_layer('provinces')['layers']
        self.assertTrue('blue-marble' in layers)
        layers = self.layers.portal_layer('blue-marble')['layers']
        self.assertFalse('blue-marble' in layers)

    def test_update_map_layer_order(self):
        args = self._emtpy_map_layer_args('blue-marble')
        args.order = 5
        self.layers.update_map_layer(args)
        layers = self.layers.root['wmsLayers']
        self.assertEqual('blue-marble', layers[len(layers) - 5]['id'])

    def test_update_map_layer_invalid_order(self):
        args = self._emtpy_map_layer_args('blue-marble')
        args.order = 9999
        try:
            self.layers.update_map_layer(args)
            self.fail()
        except Exception as e:
            pass

    def test_update_map_layer_invalid_id(self):
        args = argparse.Namespace(id='invalid')
        try:
            self.layers.update_map_layer(args)
            self.fail()
        except Exception as e:
            pass

    def test_update_map_layer_invalid_parent(self):
        args = argparse.Namespace(id='blue-marble', portal_layer='invalid')
        try:
            self.layers.update_map_layer(args)
            self.fail()
        except Exception as e:
            pass


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
