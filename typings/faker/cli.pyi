"""
This type stub file was generated by pyright.
"""

__author__ = 'joke2k'
def print_provider(doc, provider, formatters, excludes=..., output=...):
    ...

def print_doc(provider_or_field=..., args=..., lang=..., output=..., seed=..., includes=...):
    ...

class Command(object):
    def __init__(self, argv=...) -> None:
        ...
    
    def execute(self):
        """
        Given the command-line arguments, this creates a parser appropriate
        to that command, and runs it.
        """
        ...
    


def execute_from_command_line(argv=...):
    """A simple method that runs a Command."""
    ...
