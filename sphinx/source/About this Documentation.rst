About this Documentation
========================

**Generating the documentation**

We use sphinx to generate the documenation. It extracts doc-strings from the relevant python-files and combines them with the documentation from sphinx/source.

The result is saved in the docs-folder. Don't change anything here, as it will be overwritten when running the script.

To generate the documentation run `scripts/generate_documentation.sh`.


**Limitations**

There are multiple errors that can occur during generating the documentation:

1. libatlasutil.so not found

This error can be ignored.

2. modules.rst: WARNING: document isn't included in any toctree

This error can be ignored.

3. The extraction of the documentation for app.py fails

Sphinx sometimes gets confused about relative imports. Removing the dots from the import-statements in all relevant python-files might help. (Only apply this change for generating the documentation)
