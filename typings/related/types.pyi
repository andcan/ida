"""
This type stub file was generated by pyright.
"""

DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_DATETIME_FORMAT = "ISO_FORMAT"
DEFAULT_TIME_FORMAT = "%H:%M:%S"
class ImmutableDict(dict):
    def __setitem__(self, key, value):
        ...
    
    def __delitem__(self, key):
        ...
    
    def __setattr__(self, name, value):
        ...
    
    def __delattr__(self, name):
        ...
    
    def pop(self, key, **kwargs):
        ...
    
    def clear(self):
        ...
    


class TypedSequence(MutableSequence):
    """
    Custom list type that checks the instance type of new values.

    reference:
    http://stackoverflow.com/a/3488283
    """
    def __init__(self, cls, args, allow_none=...) -> None:
        ...
    
    def __str__(self) -> str:
        ...
    
    def __repr__(self):
        ...
    
    def __len__(self):
        ...
    
    def __eq__(self, other) -> bool:
        ...
    
    def __getitem__(self, i):
        ...
    
    def __delitem__(self, i):
        ...
    
    def __setitem__(self, i, v):
        ...
    
    def insert(self, i, v):
        ...
    


class TypedMapping(MutableMapping):
    """
    Custom dict type that checks the instance type of new values.

    reference:
    http://stackoverflow.com/a/3488283
    """
    def __init__(self, cls, kwargs, key=..., allow_none=...) -> None:
        ...
    
    def __str__(self) -> str:
        ...
    
    def __repr__(self):
        ...
    
    def __len__(self):
        ...
    
    def __iter__(self):
        ...
    
    def __eq__(self, other) -> bool:
        ...
    
    def __getitem__(self, i):
        ...
    
    def __delitem__(self, i):
        ...
    
    def __setitem__(self, i, v):
        ...
    
    def add(self, v, key=...):
        ...
    


class TypedSet(MutableSet):
    """
    Custom set type that checks the instance type of new values.

    reference:
    http://stackoverflow.com/a/3488283
    """
    def __init__(self, cls, args, allow_none=...) -> None:
        ...
    
    def __str__(self) -> str:
        ...
    
    def __repr__(self):
        ...
    
    def __len__(self):
        ...
    
    def __eq__(self, other) -> bool:
        ...
    
    def __iter__(self):
        ...
    
    def __contains__(self, item):
        ...
    
    def add(self, v):
        ...
    
    def discard(self, value):
        ...
    

