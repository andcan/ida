"""
This type stub file was generated by pyright.
"""

class OperatorResolver(object):
    """
    Resolves and triggers an operator based on its name identifier.

    This class is highly-coupled to `grappa.Test` and consumes `grappa.Engine`
    and `grappa.Context` in order to trigger operator resolution logic.
    """
    def __init__(self, test) -> None:
        ...
    
    def run_attribute(self, operator):
        ...
    
    def run_accessor(self, operator):
        ...
    
    def run_matcher(self, operator):
        ...
    
    def attribute_error_message(self, name):
        ...
    
    def resolve(self, name):
        ...
    


