"""
This type stub file was generated by pyright.
"""

from .base import BaseReporter

class AssertionReporter(BaseReporter):
    title = ...
    template = ...
    def get_expected(self, operator=..., defaults=...):
        ...
    
    def run(self, error):
        ...
    


