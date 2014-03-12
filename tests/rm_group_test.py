import portal
import abstract_test

class Test(abstract_test.AbstractTest):
  def __init__(self, *args, **kwargs):
    super(Test, self).__init__(*args, **kwargs)

  def getCmd(self):
    return "portal-rm-group.py"

  def testNonExistingGroup(self):
    self.callError("--id", "nonexisting")

  def testNonEmptyGroup(self):
    self.callError("--id", "base")

  def testRemove(self):
    self.call("--id", "emptygroup")
    root = portal.readPortalRoot(self.testFile)
    group = portal.findGroupById(root, "newgroup")
    self.assertIsNone(group)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
