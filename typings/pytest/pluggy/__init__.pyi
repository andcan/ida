"""
This type stub file was generated by pyright.
"""

"""
Tracing utils
"""
class TagTracer(object):
    def __init__(self) -> None:
        ...
    
    def get(self, name):
        ...
    
    def setwriter(self, writer):
        ...
    
    def setprocessor(self, tags, processor):
        ...
    


class TagTracerSub(object):
    def __init__(self, root, tags) -> None:
        ...
    
    def __call__(self, *args):
        ...
    
    def get(self, name):
        ...
    


