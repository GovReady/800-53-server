# 800-53-server
Prototype of making fisma 800-53 controls interactive

# Goal
Create a python class that generates basic information about a FISMA 800-53 security control including:
- [x] Full name of control
- [x] Who has responsibility for control (e.g., organization or information system)
- [x] Listing of control dependencies (e.g., precursor controls)
- [x] Visual depiction of control dependencies

# Warning
This is early code. The graph methods *may* have errors.

# Requirements
- Python 2.7
- xsltproc
- Graphviz

# 800-53 security control web server
Run `800-53-server.py` from root of repo on local machine

```
python web/800-53-server.py
```

Open browser and visit either below URL:
- http://127.0.0.1:8080/control
- http://127.0.0.1:8080/control?id=SA-4

### Want JSON?

http://127.0.0.1:8080/control?id=SA-4&format=json

# 800-53 security control from command line
Run `viz_control_precursor.py` from root of repo.

```
python lib/viz_control_precursor.py
```

Example output:
```
Resolve which control? AU-7
====================================
AU-7 :  ['AU-2', 'AU-3', 'AU-8', 'AU-14']
AU-7 - AUDIT REDUCTION AND REPORT GENERATION (information system)
AU-2 - AUDIT EVENTS (organization)
RA-3 - RISK ASSESSMENT (organization)
PM-9 - RISK MANAGEMENT STRATEGY (organization)
AU-3 - CONTENT OF AUDIT RECORDS (information system)
AU-8 - TIME STAMPS (information system)
AU-14 - SESSION AUDIT (information system)
   
Rendering precursor graph
nodes:  ['AU-7', 'AU-2', 'RA-3', 'PM-9', 'AU-3', 'AU-8', 'AU-14']
edges:  [('AU-2', 'AU-7'), ('AU-3', 'AU-7'), ('AU-8', 'AU-7'), ('AU-14', 'AU-7'), ('RA-3', 'AU-2'), ('PM-9', 'RA-3'), ('AU-2', 'AU-3'), ('AU-2', 'AU-8'), ('AU-2', 'AU-14')]
image: output/img/AU-7-precursors.png

```

# Testing
```
python tests/unittest_seccontrol.py 
python tests/unittest_seccontrolviz.py 
```

# Files

Files                     | Description
--------------------------|---------------------------------------------
web/800-53-server.py      | Launches Cherrypy-based web server providing 800-53 control info
lib/viz_control_precursor.py | Generates precursor list and graphviz of precursors for security control
lib/control2json.xsl      | XSL transformation that creates json version of control from 800-53.xml
lib/seccontrol.py         | Security Control class, provides information about a security control
lib/seccontrolviz.py      | Security Control Graph+Viz class, provides information about a security control dependencies
lib/parsedependencies.py  | (study) Produces dependencies of precursor security controls based on 800-53A Assessment docs
lib/vizgraph.py           | (study) Generates graphviz dot file and graphic from within python
tests/*                   | unit tests files


# Useful Links

Resource                  | Link
--------------------------|---------------------------------------------
800-53 v4 PDF             | http://dx.doi.org/10.6028/NIST.SP.800-53Ar4
800-53 v4 XML current     | https://nvd.nist.gov/static/feeds/xml/sp80053/rev4/800-53-controls.xml
800-53 A v4 XML 06-06-2015  | https://nvd.nist.gov/static/feeds/xml/sp80053/rev4/800-53a-objectives.xml
800-53 Assessment Cases (2010) | http://csrc.nist.gov/groups/SMA/fisma/assessment.html

