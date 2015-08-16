#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import sys
import os
import json
import codecs

sys.path.append(os.path.join('lib'))
from utilities import *

class TestUtitilities(unittest.TestCase):
	
	def test(self):
		self.assertTrue(True)


	def test_replace_line_breaks_slashn(self):
		""" test replacing `\n` with `<br />` """
		text = "Line 1\nLine 2\nLine 3"
		expected = "Line 1<br />Line 2<br />Line 3"
		actual = replace_line_breaks(text, "\n", "<br />")
		self.assertTrue(actual == expected)
		# test function defaults
		actual = replace_line_breaks(text)
		self.assertTrue(actual == expected)


	def test_replace_line_breaks_none(self):
		""" test replacing text with no line breaks returns original string """
		text = "Line 1 Line 2 Line 3"
		expected = "Line 1 Line 2 Line 3"
		actual = replace_line_breaks(text, "\n", "<br />")
		self.assertTrue(actual == expected)


	def test_replace_line_breaks_nonetype(self):
		""" test replacing text with no line breaks returns original string """
		text = None
		expected = ""
		actual = replace_line_breaks(text, "\n", "<br />")
		self.assertTrue(actual == expected)


	def test_replace_unicodes(self):
		""" test replacement of certain unicodes """
		text = u"Inherent in defining an organization�s information protection needs"
		expected = "Inherent in defining an organization's information protection needs"
		actual = replace_unicodes(text)
		self.assertTrue(actual ==  expected)

		
if __name__ == "__main__":
	unittest.main()
