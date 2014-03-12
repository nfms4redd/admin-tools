import portal
import abstract_test

class Test(abstract_test.AbstractTest):
  def __init__(self, *args, **kwargs):
    super(Test, self).__init__(*args, **kwargs)

  def getCmd(self):
    return "portal-add-layer.py"

  def testMissingId(self):
    self.callError("--url", "http://www.example.com", 
                   "--wmsName", "wms-name", "--label", "Label", 
                   "--group", "base")

  def testMissingUrl(self):
    self.callError("--id", "newlayer", "--wmsName", "wms-name", 
                   "--label", "Label", "--group", "base")

  def testMissingWmsName(self):
    self.callError("--id", "newlayer", "--url", "http://www.example.com", 
                   "--label", "Label", "--group", "base")

  def testMissingLabel(self):
    self.callError("--id", "newlayer", "--url", "http://www.example.com", 
                   "--wmsName", "wms-name", "--group", "base")

  def testMissingGroup(self):
    self.callError("--id", "newlayer", "--url", "http://www.example.com", 
                   "--wmsName", "wms-name", "--label", "Label")

  def testNonExistingGroup(self):
    self.callError("--id", "newlayer", "--url", "http://www.example.com", 
                   "--wmsName", "wms-name", "--label", "Label",
                   "--group", "nonexisting")

  def testAddLayer(self):
    self.call("--id", "newlayer", "--url", "http://www.example.com", 
              "--wmsName", "wms-name", "--label", "Label", 
              "--group", "base")

    root = portal.readPortalRoot(self.testFile)
    mapLayer = portal.findLayerById(root["wmsLayers"], "map-newlayer")
    portalLayer = portal.findLayerById(root["portalLayers"], "newlayer")
    group = portal.findGroupById(root, "base")

    self.assertIsNotNone(mapLayer)
    self.assertIsNotNone(portalLayer)
    self.assertEquals("http://www.example.com", mapLayer["baseUrl"])
    self.assertEquals("wms-name", mapLayer["wmsName"])
    self.assertEquals("Label", mapLayer["label"])
    self.assertEquals("Label", portalLayer["label"])
    self.assertTrue("newlayer" in group["items"])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
