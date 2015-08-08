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

	def test_node_options_by_id(self):
		id = "AU-3"
		cv = SecControlViz(id)
		node_options = cv.node_options_by_id(id)
		# print "node_options: ", node_options
		self.assertTrue(node_options == {'fontname': 'arial', 'URL': '/control?id=AU-3', 'tooltip': u'(AU-3) Content Of Audit Records', 'label': u'AU-3\nContent Of Audit Records', 'color': 'palevioletred', 'shape': 'egg', 'fontsize': '12', 'fontcolor': 'palevioletred'})

	def test_create_node_options_tuples(self):
		# To Do: Make shape and attributes passed in variables
		id = "AU-3"
		cv = SecControlViz(id)
		# Find precursor nodes
		cv.precursor_list(cv.dep_dict, id, cv.nodes)
		# print "cv.nodes: ", cv.nodes
		# print cv.node_options_tuples(cv.nodes)
		self.assertTrue(cv.node_options_tuples(cv.nodes) == [('AU-3', {'fontname': 'arial', 'URL': '/control?id=AU-3', 'tooltip': u'(AU-3) Content Of Audit Records', 'label': u'AU-3\nContent Of Audit Records', 'color': 'palevioletred', 'shape': 'egg', 'fontsize': '12', 'fontcolor': 'palevioletred'}), ('AU-2', {'fontname': 'arial', 'URL': '/control?id=AU-2', 'tooltip': u'(AU-2) Audit Events', 'label': u'AU-2\nAudit Events', 'color': 'cornflowerblue', 'shape': 'egg', 'fontsize': '12', 'fontcolor': 'cornflowerblue'}), ('RA-3', {'fontname': 'arial', 'URL': '/control?id=RA-3', 'tooltip': u'(RA-3) Risk Assessment', 'label': u'RA-3\nRisk Assessment', 'color': 'cornflowerblue', 'shape': 'egg', 'fontsize': '12', 'fontcolor': 'cornflowerblue'}), ('PM-9', {'fontname': 'arial', 'URL': '/control?id=PM-9', 'tooltip': u'(PM-9) Risk Management Strategy', 'label': u'PM-9\nRisk Management Strategy', 'color': 'cornflowerblue', 'shape': 'egg', 'fontsize': '12', 'fontcolor': 'cornflowerblue'})])

	def test_edges(self):
		id = "AU-3"
		cv = SecControlViz(id)
		cv.precursor_list(cv.dep_dict, id, cv.nodes)
		for node in cv.nodes:
			cv.precursor_edges(cv.dep_dict, node, cv.edges)
		# print "edges: ", cv.edges
		self.assertTrue(cv.edges == [(('AU-2', 'AU-3'), {'color': 'darkkhaki', 'arrowhead': 'open'}), (('RA-3', 'AU-2'), {'color': 'darkkhaki', 'arrowhead': 'open'}), (('PM-9', 'RA-3'), {'color': 'darkkhaki', 'arrowhead': 'open'})])

	def test_add_nodes(self):
		# To Do: Make shape and attributes passed in variables
		id = "AU-3"
		cv = SecControlViz(id)
		cv.precursor_list(cv.dep_dict, id, cv.nodes)
		digraph = cv.add_nodes(cv.digraph(), cv.node_options_tuples(cv.nodes))
		# print "<%s>" % digraph
		# print cv.nodes
		self.assertTrue("%s" % digraph == """digraph {
	"AU-3" [label="AU-3
Content Of Audit Records" URL="/control?id=AU-3" color=palevioletred fontcolor=palevioletred fontname=arial fontsize=12 shape=egg tooltip="(AU-3) Content Of Audit Records"]
	"AU-2" [label="AU-2
Audit Events" URL="/control?id=AU-2" color=cornflowerblue fontcolor=cornflowerblue fontname=arial fontsize=12 shape=egg tooltip="(AU-2) Audit Events"]
	"RA-3" [label="RA-3
Risk Assessment" URL="/control?id=RA-3" color=cornflowerblue fontcolor=cornflowerblue fontname=arial fontsize=12 shape=egg tooltip="(RA-3) Risk Assessment"]
	"PM-9" [label="PM-9
Risk Management Strategy" URL="/control?id=PM-9" color=cornflowerblue fontcolor=cornflowerblue fontname=arial fontsize=12 shape=egg tooltip="(PM-9) Risk Management Strategy"]
}"""
)

	def test_add_edges(self):
		id = "AU-3"
		cv = SecControlViz(id)
		cv.precursor_list(cv.dep_dict, id, cv.nodes)
		# create edges
		for node in cv.nodes:
			cv.precursor_edges(cv.dep_dict, node, cv.edges)
		digraph = cv.add_nodes(cv.digraph(), cv.node_options_tuples(cv.nodes))
		# print "<%s>" % digraph

		# weak test, first delete file if exists
		try:
		    os.remove("output/img/%s-precursors" % id)
		    os.remove("output/img/%s-precursors.%s" % (id, cv.vizformat))
		except OSError:
		    pass
		# generate graphviz file
		cv.add_edges(cv.add_nodes(cv.digraph(), cv.node_options_tuples(cv.nodes)),
			cv.edges
		).render("output/img/%s-precursors" % id)
		print "image: output/img/%s-precursors.%s" % (id, cv.vizformat)
		# now see if image file created?
		self.assertTrue(os.path.exists("output/img/%s-precursors.%s" % (id, cv.vizformat)))
		
if __name__ == "__main__":
	unittest.main()
