🙏 Aim
======

This library is used to create lots of test data based on a very human-readable yaml file. Sargilo is meant to be agnostic to which framework or ORM you use, but will provide a basic configuration for Django, as this was the primary reason for writing this library.

Goals:
- [ ] Declare data in human-readable format (yaml preferred)
- [ ] Work with any data type (including datetimes (date, datetime, timedelta), email, files, enums, JSON)
- [ ] Add metadata to data (e.g. unauthorized user, standard user, etc.)
- [ ] Entries have to be linked together (maybe ForeignKeys can be declared backwards from the referenced object as arrays)
- [ ] Test data has to be accessible by attribute access (dictionary lookups are ugly and a pain to write)
- [ ] Python test data must have code completion (generate class with typings?)
- [ ] Integrate with Django and unittest (standard and behave)
- [ ] Syntax to define asset folder (maybe on per resource base)
- [ ] Options to add extra data (e.g. files) for testing with metadata
- [ ] Option to import all data with one command into shell