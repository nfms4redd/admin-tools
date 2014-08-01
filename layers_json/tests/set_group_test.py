import portal
import abstract_test

class Test(abstract_test.AbstractTest):
  def __init__(self, *args, **kwargs):
    super(Test, self).__init__(*args, **kwargs)

  def getCmd(self):
    return "portal-set-group.py"

  def testNonExistingGroup(self):
    self.callError("--id", "nonexisting", "--label", "newlabel")

  def testMissingArgs(self):
    self.callError("--id", "base")

  def testChangeParent(self):
    self.call("--id", "innerbase", "--parent", "root")
    root = portal.readPortalRoot(self.testFile)
    parent = portal.findGroupParent(root, "innerbase")
    self.assertEquals("root", parent["id"])

  def testChangeLabel(self):
    self.call("--id", "innerbase", "--label", "New Label")
    root = portal.readPortalRoot(self.testFile)
    group = portal.findGroupById(root, "innerbase")
    self.assertEquals("New Label", group["label"])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
