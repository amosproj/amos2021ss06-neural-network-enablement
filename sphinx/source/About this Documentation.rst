About this Documentation
========================

**Generating the documentation**

The documentation sources are located in sphinx/source. The python doc-strings are extracted automatically using sphinx.

One can generate the documentation by running `scripts/generate_documentation.sh`

**Limitations**

There are multiple errors that can occur during generating the documentation:

1. libatlasutil.so not found

This error can be ignored.

2. The extraction of the documentation for app.py fails

Sphinx sometimes gets confused about relative imports. Removing the dots from the import-statements in all relevant python-files might help. (Only apply this change for generating the documentation)
