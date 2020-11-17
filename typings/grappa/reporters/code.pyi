"""
This type stub file was generated by pyright.
"""

from .base import BaseReporter

class Trace(object):
    """
    Python < 3.4 traceback compatibility wrapper for Python +3.5
    """
    def __init__(self, trace) -> None:
        ...
    


class CodeReporter(BaseReporter):
    """
    CodeReporter matches and renders the fragment of the code
    """
    title = ...
    LINES = ...
    INDENT_SPACES = ...
    PIPE_EXPR = ...
    FN_CALL_EXPR = ...
    CONTEXT_EXPR = ...
    def match_line(self, line):
        ...
    
    def find_trace(self):
        ...
    
    def header(self, trace):
        ...
    
    def render_code(self, trace):
        ...
    
    def run(self, error):
        ...
    


