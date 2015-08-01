#!/usr/bin/python
"""Class for 800-53 Security Controls

Instantiate class with Security Control ID (e.g., AT-2, CM-3).

Methods provide information about the Security Control.


This program is part of research for Homeland Open Security Technologies to better
understand how to map security controls to continuous monitoring.

Visit [tbd] for the latest version.
"""

__author__ = "Greg Elin (gregelin@gitmachines.com)"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2015/08/01 13:07:00 $"
__copyright__ = "Copyright (c) 2015 GovReady PBC"
__license__ = "GPL 3.0"

import os
import sys
import json
import commands
import re

class SecControl(object):
    "represent 800-53 security controls"
    
    def __init__(self, id):
        self.id = id

        # Load control information
        results = commands.getstatusoutput("xsltproc --stringparam controlnumber %s lib/control2json.xsl data/800-53-controls.xml" % self.id)
        if results[0] == 0:
            if len(results[1]) > 0:
                # Command ran successfully
                self.details = json.loads(results[1])
                self.title = self.details["title"]
                self.description = self.details["description"]
            else:
                # Raise error because we got a blank
                self.details = json.loads('{"id": "xx", "error": "Failed to get security control information from 800-53 xml"}')
                self.title = "Error"
                self.description = "Error"
        else:
            # Error, failed to execute command
            self.details = json.loads('{"id": "xx", "error": "Failed to get security control information from 800-53 xml"}')
            self.title = "Error"
            self.description = "Error"
        
    def get_control_json(self):
        print json.dumps(self.details)

    def getResponsible(self):
        m = re.match(r'The organization|The information system', self.description)
        if m.group(0) == "The organization":
            return "organization"
        else:
            if m.group(0) == "The information system":
                return "information system"
            else:
                return "other"


# if __name__ == "__main__":
#     print "Class SecControl"
