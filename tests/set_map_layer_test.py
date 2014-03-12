import portal
import abstract_test
import os
import shutil

class Test(abstract_test.AbstractTest):
  def __init__(self, *args, **kwargs):
    super(Test, self).__init__(*args, **kwargs)

  def getCmd(self):
    return "portal-set-map-layer.py"

  def testMissingId(self):
    self.callError()

  def testChangeUrl(self):
    self.call("--id", "blue-marble", "--url", "http://www.example.com")

    root = portal.readPortalRoot(self.testFile)
    mapLayer = portal.findLayerById(root["wmsLayers"], "blue-marble")
    self.assertEquals("http://www.example.com", mapLayer["baseUrl"])

  def testChangeWmsName(self):
    self.call("--id", "blue-marble", "--wmsName", "wms-name")

    root = portal.readPortalRoot(self.testFile)
    mapLayer = portal.findLayerById(root["wmsLayers"], "blue-marble")
    self.assertEquals("wms-name", mapLayer["wmsName"])

  def testChangeWmsTime(self):
    self.call("--id", "blue-marble", "--wmsTime", "time")

    root = portal.readPortalRoot(self.testFile)
    mapLayer = portal.findLayerById(root["wmsLayers"], "blue-marble")
    self.assertEquals("time", mapLayer["wmsTime"])

  def testChangeImageFormat(self):
    self.call("--id", "blue-marble", "--imageFormat", "image/jpeg")

    root = portal.readPortalRoot(self.testFile)
    mapLayer = portal.findLayerById(root["wmsLayers"], "blue-marble")
    self.assertEquals("image/jpeg", mapLayer["imageFormat"])

  def testChangeSourceLabel(self):
    self.call("--id", "blue-marble", "--sourceLabel", "Source Label")

    root = portal.readPortalRoot(self.testFile)
    mapLayer = portal.findLayerById(root["wmsLayers"], "blue-marble")
    self.assertEquals("Source Label", mapLayer["sourceLabel"])

  def testChangeSourceLink(self):
    self.call("--id", "blue-marble", "--sourceLink", "http://www.source.com")

    root = portal.readPortalRoot(self.testFile)
    mapLayer = portal.findLayerById(root["wmsLayers"], "blue-marble")
    self.assertEquals("http://www.source.com", mapLayer["sourceLink"])

  def testChangeLabel(self):
    self.call("--id", "blue-marble", "--label", "Label")

    root = portal.readPortalRoot(self.testFile)
    mapLayer = portal.findLayerById(root["wmsLayers"], "blue-marble")
    self.assertEquals("Label", mapLayer["label"])

  def testChangeLegendMissingLang(self):
    self.callError("--id", "blue-marble", "--legend", "sample_legend.png")

  def testChangeLegendMissingFile(self):
    self.callError("--id", "blue-marble", "--legend", "non_existing_file.png", "--lang", "es")

  def testChangeLegend(self):
    self.call("--id", "blue-marble", "--legend", self.getPath('sample_legend.png'), "--lang", "es")

    root = portal.readPortalRoot(self.testFile)
    mapLayer = portal.findLayerById(root["wmsLayers"], "blue-marble")

    path = portal.getLocalizedDir(self.testFile, "es", "images")
    self.assertTrue(os.path.isfile(os.path.join(path, "blue-marble.png")))
    self.assertEquals("blue-marble.png", mapLayer["legend"])

    shutil.rmtree(self.getPath('static'))

  def testChangeQueryable(self):
    self.call("--id", "blue-marble", "--queryable")
    root = portal.readPortalRoot(self.testFile)
    mapLayer = portal.findLayerById(root["wmsLayers"], "blue-marble")
    self.assertTrue(mapLayer["queryable"])

  def testChangeNotQueryable(self):
    self.call("--id", "blue-marble", "--not-queryable")
    root = portal.readPortalRoot(self.testFile)
    mapLayer = portal.findLayerById(root["wmsLayers"], "blue-marble")
    self.assertFalse(mapLayer["queryable"])

  def testConflictQueryableArgs(self):
    self.callError("--id", "blue-marble", "--queryable", "--not-queryable")

  def testChangeHidden(self):
    self.call("--id", "blue-marble", "--hidden")
    root = portal.readPortalRoot(self.testFile)
    mapLayer = portal.findLayerById(root["wmsLayers"], "blue-marble")
    self.assertFalse(mapLayer["visible"])

  def testChangeNotHidden(self):
    self.call("--id", "blue-marble", "--not-hidden")
    root = portal.readPortalRoot(self.testFile)
    mapLayer = portal.findLayerById(root["wmsLayers"], "blue-marble")
    self.assertTrue(mapLayer["visible"])

  def testConflictHiddenArgs(self):
    self.callError("--id", "blue-marble", "--hidden", "--not-hidden")

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
