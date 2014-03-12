import portal
import abstract_test

class Test(abstract_test.AbstractTest):
  def __init__(self, *args, **kwargs):
    super(Test, self).__init__(*args, **kwargs)

  def getCmd(self):
    return "portal-rm-map-layer.py"

  def testMissingId(self):
    self.callError()

  def testOnlyOneMapLayerPerPortalLayer(self):
    self.callError("--id", "blue-marble")

  def testRemove(self):
    self.call("--id", "forestClassification2")

    root = portal.readPortalRoot(self.testFile)
    portalLayer = portal.findLayerById(root["portalLayers"], "forestClassification")
    self.assertIsNone(portal.findLayerById(root["wmsLayers"], "forestClassification2"))
    self.assertFalse("forestClassification2" in portalLayer["layers"])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
