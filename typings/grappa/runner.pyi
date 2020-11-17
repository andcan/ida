"""
This type stub file was generated by pyright.
"""

class Runner(object):
    """
    Runner is responsible of triggering the registed assertion operators in the
    current engine.

    Arguments:
        engine (grappa.Engine)
    """
    def __init__(self, engine) -> None:
        ...
    
    def render_error(self, ctx, error):
        ...
    
    def run_assertions(self, ctx):
        ...
    
    def run(self, ctx):
        """
        Runs the current phase.
        """
        ...
    


