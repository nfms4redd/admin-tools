import portal
import abstract_test
import os
import shutil

class Test(abstract_test.AbstractTest):
  def __init__(self, *args, **kwargs):
    super(Test, self).__init__(*args, **kwargs)

  def getCmd(self):
    return "portal-set-layer.py"

  def testMissingId(self):
    self.callError()

  def testChangeMapLayerUrl(self):
    self.call("--id", "blue-marble", "--url", "http://www.example.com")

    root = portal.readPortalRoot(self.testFile)
    mapLayer = portal.findLayerById(root["wmsLayers"], "blue-marble")
    self.assertEquals("http://www.example.com", mapLayer["baseUrl"])

  def testChangeMoreThanOneMapLayer(self):
    self.callError("--id", "forestClassification", "--wmsName", "wms-name")

  def testChangeStartVisible(self):
    self.call("--id", "blue-marble", "--start-visible")
    root = portal.readPortalRoot(self.testFile)
    portalLayer = portal.findLayerById(root["portalLayers"], "blue-marble")
    self.assertTrue(portalLayer["active"])

  def testChangeStartInvisible(self):
    self.call("--id", "blue-marble", "--start-invisible")
    root = portal.readPortalRoot(self.testFile)
    portalLayer = portal.findLayerById(root["portalLayers"], "blue-marble")
    self.assertFalse(portalLayer["active"])

  def testConflictVisibleArgs(self):
    self.callError("--id", "blue-marble", "--start-visible", "--start-invisible")

  def testChangeInfoFileMissingLang(self):
    self.callError("--id", "blue-marble", "--infoFile", self.getPath('sample_info.html'))

  def testChangeInfoFileMissingFile(self):
    self.callError("--id", "blue-marble", "--legend", "non_existing_file.html", "--lang", "es")

  def testChangeInfoFile(self):
    self.call("--id", "blue-marble", "--infoFile", self.getPath('sample_info.html'), "--lang", "es")

    root = portal.readPortalRoot(self.testFile)
    portalLayer = portal.findLayerById(root["portalLayers"], "blue-marble")

    path = portal.getLocalizedDir(self.testFile, "es", "html")
    self.assertTrue(os.path.isfile(os.path.join(path, "blue-marble.html")))
    self.assertEquals("blue-marble.html", portalLayer["infoFile"])

    shutil.rmtree(self.getPath('static'))

  def testChangeLabel(self):
    self.call("--id", "blue-marble", "--label", "Label")

    root = portal.readPortalRoot(self.testFile)
    mapLayer = portal.findLayerById(root["wmsLayers"], "blue-marble")
    portalLayer = portal.findLayerById(root["portalLayers"], "blue-marble")
    self.assertEquals("Label", mapLayer["label"])
    self.assertEquals("Label", portalLayer["label"])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
