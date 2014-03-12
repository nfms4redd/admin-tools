import portal
import abstract_test

class Test(abstract_test.AbstractTest):
  def __init__(self, *args, **kwargs):
    super(Test, self).__init__(*args, **kwargs)

  def getCmd(self):
    return "portal-add-map-layer.py"

  def testMissingId(self):
    self.callError("--url", "http://www.example.com", 
                   "--wmsName", "wms-name", "--label", "Label", 
                   "--portalLayer", "forest_mask")

  def testMissingUrl(self):
    self.callError("--id", "newmaplayer", "--wmsName", "wms-name", 
                   "--label", "Label", "--portalLayer", "forest_mask")

  def testMissingWmsName(self):
    self.callError("--id", "newmaplayer", "--url", "http://www.example.com", 
                   "--label", "Label", "--portalLayer", "forest_mask")

  def testMissingLabel(self):
    self.callError("--id", "newmaplayer", "--url", "http://www.example.com", 
                   "--wmsName", "wms-name", "--portalLayer", "forest_mask")

  def testMissingPortalLayer(self):
    self.callError("--id", "newmaplayer", "--url", "http://www.example.com", 
                   "--wmsName", "wms-name", "--label", "Label")

  def testNonExistingPortalLayer(self):
    self.callError("--id", "newmaplayer", "--url", "http://www.example.com", 
                   "--wmsName", "wms-name", "--label", "Label",
                   "--portal-layer", "nonexisting")

  def testAddMapLayer(self):
    self.call("--id", "newmaplayer", "--url", "http://www.example.com", 
              "--wmsName", "wms-name", "--label", "Label", 
              "--portal-layer", "forest_mask")

    root = portal.readPortalRoot(self.testFile)
    mapLayer = portal.findLayerById(root["wmsLayers"], "newmaplayer")
    portalLayer = portal.findLayerById(root["portalLayers"], "forest_mask")

    self.assertIsNotNone(mapLayer)
    self.assertEquals("http://www.example.com", mapLayer["baseUrl"])
    self.assertEquals("wms-name", mapLayer["wmsName"])
    self.assertEquals("Label", mapLayer["label"])
    self.assertTrue("newmaplayer" in portalLayer["layers"])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
