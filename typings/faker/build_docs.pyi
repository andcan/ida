"""
This type stub file was generated by pyright.
"""

import os

DOCS_ROOT = os.path.abspath(os.path.join('..', 'docs'))
def write(fh, s):
    ...

def write_base_provider(fh, doc, base_provider):
    ...

def write_provider(fh, doc, provider, formatters, excludes=...):
    ...

def write_docs(*args, **kwargs):
    ...

def setup(app):
    ...

if __name__ == "__main__":
    ...
