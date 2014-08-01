import portal
import abstract_test

class Test(abstract_test.AbstractTest):
  def __init__(self, *args, **kwargs):
    super(Test, self).__init__(*args, **kwargs)

  def getCmd(self):
    return "portal-rm-layer.py"

  def testMissingId(self):
    self.callError()

  def testNonExisting(self):
    self.callError("--id", "nonexisting")

  def testRemove(self):
    self.call("--id", "blue-marble")

    root = portal.readPortalRoot(self.testFile)
    group = portal.findGroupById(root, "innerbase")
    self.assertIsNone(portal.findLayerById(root["portalLayers"], "blue-marble"))
    self.assertIsNone(portal.findLayerById(root["wmsLayers"], "blue-marble"))
    self.assertFalse("blue-marble" in group["items"])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
