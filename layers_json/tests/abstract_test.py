import os
import shutil
import subprocess
import unittest

DIR = os.path.dirname(os.path.realpath(__file__))
TEST = os.path.join(DIR, "test.json")
LAYERS = os.path.join(DIR, "layers.json")

class AbstractTest(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(AbstractTest, self).__init__(*args, **kwargs)
    self.testFile = TEST

  def setUp(self):
    shutil.copyfile(LAYERS, TEST)

  def call(self, *args):
    status = subprocess.call(self.cmd() + list(args), 
                           stdout=open(os.devnull, 'wb'))
    self.assertEquals(0, status)

  def callError(self, *args):
    status = subprocess.call(self.cmd() + list(args), 
                           stdout=open(os.devnull, 'wb'),
                           stderr=open(os.devnull, 'wb'))
    self.assertNotEquals(0, status)

  def cmd(self):
    return [os.path.join(DIR, "..", self.getCmd()), "--file", TEST]

  def getCmd(self):
    pass

  def getPath(self, path):
    return os.path.join(DIR, path)
