"""
This type stub file was generated by pyright.
"""

from .compat import PY2

FACTORY_REPLACE = { type(object.__dict__): dict,type({  }.keys()): list,type({  }.values()): list,type({  }.items()): list }
def empty(coll):
    """Creates an empty collection of the same type."""
    ...

if PY2:
    def iteritems(coll):
        ...
    
    def itervalues(coll):
        ...
    
else:
    def iteritems(coll):
        ...
    
    def itervalues(coll):
        ...
    
def join(colls):
    """Joins several collections of same type into one."""
    ...

def merge(*colls):
    """Merges several collections of same type into one.

    Works with dicts, sets, lists, tuples, iterators and strings.
    For dicts later values take precedence."""
    ...

def join_with(f, dicts):
    """Joins several dicts, combining values with given function."""
    ...

def merge_with(f, *dicts):
    """Merges several dicts, combining values with given function."""
    ...

def walk(f, coll):
    """Walks the collection transforming its elements with f.
       Same as map, but preserves coll type."""
    ...

def walk_keys(f, coll):
    """Walks keys of the collection, mapping them with f."""
    ...

def walk_values(f, coll):
    """Walks values of the collection, mapping them with f."""
    ...

def select(pred, coll):
    """Same as filter but preserves coll type."""
    ...

def select_keys(pred, coll):
    """Select part of the collection with keys passing pred."""
    ...

def select_values(pred, coll):
    """Select part of the collection with values passing pred."""
    ...

def compact(coll):
    """Removes falsy values from the collection."""
    ...

def is_distinct(coll, key=...):
    """Checks if all elements in the collection are different."""
    ...

def all(pred, seq=...):
    """Checks if all items in seq pass pred (or are truthy)."""
    ...

def any(pred, seq=...):
    """Checks if any item in seq passes pred (or is truthy)."""
    ...

def none(pred, seq=...):
    """"Checks if none of the items in seq pass pred (or are truthy)."""
    ...

def one(pred, seq=...):
    """Checks whether exactly one item in seq passes pred (or is truthy)."""
    ...

def some(pred, seq=...):
    """Finds first item in seq passing pred or first that is truthy."""
    ...

def zipdict(keys, vals):
    """Creates a dict with keys mapped to the corresponding vals."""
    ...

def flip(mapping):
    """Flip passed dict or collection of pairs swapping its keys and values."""
    ...

def project(mapping, keys):
    """Leaves only given keys in mapping."""
    ...

def omit(mapping, keys):
    """Removes given keys from mapping."""
    ...

def zip_values(*dicts):
    """Yields tuples of corresponding values of several dicts."""
    ...

def zip_dicts(*dicts):
    """Yields tuples like (key, val1, val2, ...)
       for each common key in all given dicts."""
    ...

def get_in(coll, path, default=...):
    """Returns a value at path in the given nested collection."""
    ...

def set_in(coll, path, value):
    """Creates a copy of coll with the value set at path."""
    ...

def update_in(coll, path, update, default=...):
    """Creates a copy of coll with a value updated at path."""
    ...

def lwhere(mappings, **cond):
    """Selects mappings containing all pairs in cond."""
    ...

def lpluck(key, mappings):
    """Lists values for key in each mapping."""
    ...

def lpluck_attr(attr, objects):
    """Lists values of given attribute of each object."""
    ...

def linvoke(objects, name, *args, **kwargs):
    """Makes a list of results of the obj.name(*args, **kwargs)
       for each object in objects."""
    ...

def where(mappings, **cond):
    """Iterates over mappings containing all pairs in cond."""
    ...

def pluck(key, mappings):
    """Iterates over values for key in mappings."""
    ...

def pluck_attr(attr, objects):
    """Iterates over values of given attribute of given objects."""
    ...

def invoke(objects, name, *args, **kwargs):
    """Yields results of the obj.name(*args, **kwargs)
       for each object in objects."""
    ...

