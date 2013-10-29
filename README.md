LogChronicle
============

Log Chronicle


Q: Why another logging project?
A: Various logging modules provide differing levels of features and
documentation.  None of the logging alternatives researched provided the full
set of features desired thus this simple logging project was created.

What features?

* Ability to easily mark information as confidential log data (for admins only)
    and easily filter out this confidential data out of logs before allowing
    customers to view them
    - Example: Logging exceptions sounds like a great idea but there can be 
        cases where a database exception might hold credential data.
* Automatic support for addition of file and line number into logs
* Support for basically any Python data type as a log entity
* JSON log output
* Ability to bind data to the log class and carry it forward to be logged
    automatically later (see examples for details in test.py)
* Maintain log state and binds across modules
* Basic logging features look/act like/are Python Logging compatible


Log Chronicle usage is shown and documented in test.py (which calls test2.py
for multi-module support examples).
