# fisma-800-53-control
Prototype of making fisma 800-53 controls interactive

# Goal
Create a python class that generates basic information about a FISMA 800-53 security control including:
- [x] Full name of control
- [x] Who has responsibility for control (e.g., organization or information system)
- [-] Listing of control dependencies (e.g., precursor controls)
- [ ] Visual depiction of control dependencies

# Testing
```
python tests/unittest_seccontrol.py 
```

# List dependencies of a control
Run `parsedependencies.py` from root of repo.

```
python lib/parsedependencies.py
```

Example output:
```
 ====== Dependency graph loaded ========

Resolve which control? AU-7
====================================
AU-7 - AUDIT REDUCTION AND REPORT GENERATION (information system)
AU-2 - AUDIT EVENTS (organization)
RA-3 - RISK ASSESSMENT (organization)
PM-9 - RISK MANAGEMENT STRATEGY (organization)
AU-3 - CONTENT OF AUDIT RECORDS (information system)
AU-8 - TIME STAMPS (information system)
AU-14 - SESSION AUDIT (information system)
```

# Useful Links

Resource                  | Link
--------------------------|---------------------------------------------
800-53 v4 PDF             | http://dx.doi.org/10.6028/NIST.SP.800-53Ar4
800-53 v4 XML current     | https://nvd.nist.gov/static/feeds/xml/sp80053/rev4/800-53-controls.xml
800-53 A v4 XML 06-06-2015  | https://nvd.nist.gov/static/feeds/xml/sp80053/rev4/800-53a-objectives.xml
800-53 Assessment Cases (2010) | http://csrc.nist.gov/groups/SMA/fisma/assessment.html

