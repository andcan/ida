"""
This type stub file was generated by pyright.
"""

from .compat import PY2

class SkipMemoization(Exception):
    ...


def memoize(*args, **kwargs):
    """@memoize(key_func=None). Makes decorated function memoize its results.

    If key_func is specified uses key_func(*func_args, **func_kwargs) as memory key.
    Otherwise uses args + tuple(sorted(kwargs.items()))

    Exposes its memory via .memory attribute.
    """
    ...

make_lookuper = _make_lookuper(False)
silent_lookuper = _make_lookuper(True)
def cache(timeout, key_func=...):
    """Caches a function results for timeout seconds."""
    ...

if PY2:
    def has_arg_types(func):
        ...
    
else:
    def has_arg_types(func):
        ...
    
