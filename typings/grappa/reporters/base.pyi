"""
This type stub file was generated by pyright.
"""

class BaseReporter(object):
    def __init__(self, ctx, error) -> None:
        ...
    
    def cut(self, value, size=...):
        ...
    
    def linefy(self, value):
        ...
    
    def indentify(self, value):
        ...
    
    def normalize(self, value, size=..., use_raw=...):
        ...
    
    def safe_length(self, value):
        ...
    
    def from_operator(self, name, defaults=..., operator=...):
        ...
    
    def render_tmpl(self, tmpl, value):
        ...
    
    def run(self, error):
        ...
    


