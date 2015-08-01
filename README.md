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