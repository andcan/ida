"""
This type stub file was generated by pyright.
"""

from tornado.platform import interface

"""Posix implementations of platform-specific functionality."""
def set_close_exec(fd):
    ...

class Waker(interface.Waker):
    def __init__(self) -> None:
        ...
    
    def fileno(self):
        ...
    
    def write_fileno(self):
        ...
    
    def wake(self):
        ...
    
    def consume(self):
        ...
    
    def close(self):
        ...
    


