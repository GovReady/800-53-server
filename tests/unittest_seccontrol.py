import unittest
import sys
import os
import json

sys.path.append(os.path.join('lib'))
sys.path.append(os.path.join('data'))
from seccontrol import SecControl

class SecControlTest(unittest.TestCase):
	
	def test(self):
		self.assertTrue(True)

	def test_id(self):
		id = "AT-3"
		c = SecControl(id)
		self.assertTrue(id == c.id)

	def test_details(self):
		id = "AT-3"
		c = SecControl(id)
		self.assertTrue(c.title == "ROLE-BASED SECURITY TRAINING")		

	def test_details_nonexistent_control(self):
		id = "AX-3"
		c = SecControl(id)
		self.assertTrue(c.title == "Error")		



if __name__ == "__main__":
	unittest.main()
