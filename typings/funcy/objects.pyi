"""
This type stub file was generated by pyright.
"""

from .compat import PY2

class cached_property(object):
    """
    Decorator that converts a method with a single self argument into
    a property cached on the instance.
    """
    fset = ...
    def __init__(self, fget) -> None:
        ...
    
    def __get__(self, instance, type=...):
        ...
    


class cached_readonly(cached_property):
    """Same as @cached_property, but protected against rewrites."""
    def __set__(self, instance, value):
        ...
    


def wrap_prop(ctx):
    """Wrap a property accessors with a context manager"""
    ...

def monkey(cls, name=...):
    """
    Monkey patches class or module by adding to it decorated function.

    Anything overwritten could be accessed via .original attribute of decorated object.
    """
    ...

class namespace_meta(type):
    def __new__(cls, name, bases, attrs):
        ...
    


class namespace(object):
    """A base class that prevents its member functions turning into methods."""
    if PY2:
        __metaclass__ = ...


class LazyObject(object):
    """
    A simplistic lazy init object.
    Rewrites itself when any attribute is accessed.
    """
    def __init__(self, init) -> None:
        ...
    
    def __getattr__(self, name):
        ...
    
    def __setattr__(self, name, value):
        ...
    


