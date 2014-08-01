import portal
import abstract_test

class Test(abstract_test.AbstractTest):
  def __init__(self, *args, **kwargs):
    super(Test, self).__init__(*args, **kwargs)

  def getCmd(self):
    return "portal-add-group.py"

  def testAlreadyExistingGroup(self):
    self.callError("--id", "base", "--parent", "root", "--label", "lbl1")

  def testMissingParent(self):
    self.callError("--id", "newgroup", "--parent", "nonexisting", "--label", "lbl1")

  def testAddGroup(self):
    self.call("--id", "newgroup", "--parent", "base", "--label", "lbl1")

    root = portal.readPortalRoot(self.testFile)
    group = portal.findGroupById(root, "newgroup")

    self.assertIsNotNone(group)
    self.assertEquals(0, len(group["items"]))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
