import unittest
import sys
import os
import json

sys.path.append(os.path.join('lib'))
sys.path.append(os.path.join('data'))
from seccontrol import SecControl
from seccontrolviz import SecControlViz

class SecControlVizTest(unittest.TestCase):
	
	def test(self):
		self.assertTrue(True)

	def test_id(self):
		id = "AT-3"
		cv = SecControlViz(id)
		self.assertTrue(id == cv.id)

	def test_loading_graph(self):
		id = "AT-3"
		cv = SecControlViz(id)
		self.assertTrue(id == cv.id)
		dict = cv._load_graph_from_dependency_files()
		self.assertTrue(dict['AT-4'] == ['AT-2', 'AT-3'])

	def test_get_title(self):
		id = "CA-5"
		c = SecControl(id)
		cv = SecControlViz(id)
		self.assertTrue("PLAN OF ACTION AND MILESTONES" == c.title)

	def test_resolve_control_to_list(self):
		id = "AU-3"
		c = SecControl(id)
		cv = SecControlViz(id)
		cv.dep_resolve(cv.dep_dict, id, cv.resolved)
		# print "precursors: ", cv.resolved
		self.assertTrue(cv.resolved == ['RA-3', 'AU-2', 'AU-3'])

	def test_precursor_list(self):
		id = "AU-3"
		cv = SecControlViz(id)
		cv.precursor_list(cv.dep_dict, id, cv.nodes)
		# print "nodes: ", cv.nodes
		self.assertTrue(cv.nodes == ['AU-3', 'AU-2', 'RA-3', 'PM-9'])

	def test_setting_node_options_by_id(self):
		id = "AU-3"
		cv = SecControlViz(id)
		node_options = cv.node_options_by_id(id)
		# print "node_options: ", node_options
		self.assertTrue(node_options == {'fontname': 'arial', 'color': 'red', 'label': u'AU-3\nCONTENT OF AUDIT RECORDS', 'shape': 'box3d', 'fontsize': '12', 'fontcolor': 'red'})



if __name__ == "__main__":
	unittest.main()
