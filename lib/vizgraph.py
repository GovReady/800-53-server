#!/usr/bin/python
"""A script for generating graph images with graphviz

Requires graphviz module:
pip install graphviz

Run from project root.

usage: python lib/vizgraph.py

tutorial: http://matthiaseisen.com/articles/graphviz/

"""
import re
import os
import sys
import pprint
import graphviz as gv

import functools
graph = functools.partial(gv.Graph, format='svg')
digraph = functools.partial(gv.Digraph, format='svg')

def add_nodes(graph, nodes):
	for n in nodes:
		if isinstance(n, tuple):
			graph.node(n[0], **n[1])
		else:
			graph.node(n)
	return graph

def add_edges(graph, edges):
	for e in edges:
		if isinstance(e[0], tuple):
			graph.edge(*e[0], **e[1])
		else:
			graph.edge(*e)
	return graph

add_edges(
    add_nodes(digraph(), ['A', 'B', 'C']),
    [('A', 'B'), ('A', 'C'), ('B', 'C')]
).render('img/g4')

add_edges(
    add_nodes(digraph(), ['AU-5', 'AU-2', 'RA-3', 'PM-9', 'AU-3', 'AU-8', 'AU-14']),
    [('AU-2', 'AU-5'), ('AU-3', 'AU-5'), ('AU-8', 'AU-5'), ('AU-14', 'AU-5'),
    ('RA-3', 'AU-2'),
    ('AU-2', 'AU-3'), ('AU-2', 'AU-8'), ('AU-2', 'AU-14'),
    ('PM-9', 'RA-3') ]
).render('output/img/AU-5-precursors')

