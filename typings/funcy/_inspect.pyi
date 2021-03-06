"""
This type stub file was generated by pyright.
"""

import types
from .compat import PY2

ARGS = {  }
builtins_name = '__builtin__' if PY2 else 'builtins'
two_arg_funcs = '''cmp coerce delattr divmod filter getattr hasattr isinstance issubclass
                   map pow reduce'''
two_arg_funcs = 'dropwhile filterfalse ifilter ifilterfalse starmap takewhile'
two_arg_funcs = """
    _compare_digest add and_ concat contains countOf delitem div eq floordiv ge getitem
    gt iadd iand iconcat idiv ifloordiv ilshift imatmul imod imul indexOf ior ipow irepeat
    irshift is_ is_not isub itruediv ixor le lshift lt matmul mod mul ne or_ pow repeat rshift
    sequenceIncludes sub truediv xor
"""
STD_MODULES = set(ARGS)
type_classes = (type, types.ClassType) if hasattr(types, 'ClassType') else type
def get_spec(func, _cache=...):
    ...

