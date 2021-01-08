"""
This type stub file was generated by pyright.
"""

import inspect
import warnings
import attr
import six
from collections import namedtuple
from operator import attrgetter
from ..compat import ATTRS_EQ_FIELD, MappingMixin, NOTSET, ascii_escaped, getfslineno
from _pytest.deprecated import PYTEST_PARAM_UNKNOWN_KWARGS
from _pytest.outcomes import fail
from _pytest.warning_types import PytestUnknownMarkWarning

EMPTY_PARAMETERSET_OPTION = "empty_parameter_set_mark"
def alias(name, warning=...):
    ...

def istestfunc(func):
    ...

def get_empty_parameterset_mark(config, argnames, func):
    ...

class ParameterSet(namedtuple("ParameterSet", "values, marks, id")):
    @classmethod
    def param(cls, *values, **kwargs):
        ...
    
    @classmethod
    def extract_from(cls, parameterset, force_tuple=...):
        """
        :param parameterset:
            a legacy style parameterset that may or may not be a tuple,
            and may or may not be wrapped into a mess of mark objects

        :param force_tuple:
            enforce tuple wrapping so single argument tuple values
            don't get decomposed and break tests
        """
        ...
    


@attr.s(frozen=True)
class Mark(object):
    name = ...
    args = ...
    kwargs = ...
    def combined_with(self, other):
        """
        :param other: the mark to combine with
        :type other: Mark
        :rtype: Mark

        combines by appending args and merging the mappings
        """
        ...
    


@attr.s
class MarkDecorator(object):
    """ A decorator for test functions and test classes.  When applied
    it will create :class:`MarkInfo` objects which may be
    :ref:`retrieved by hooks as item keywords <excontrolskip>`.
    MarkDecorator instances are often created like this::

        mark1 = pytest.mark.NAME              # simple MarkDecorator
        mark2 = pytest.mark.NAME(name1=value) # parametrized MarkDecorator

    and can then be applied as decorators to test functions::

        @mark2
        def test_function():
            pass

    When a MarkDecorator instance is called it does the following:
      1. If called with a single class as its only positional argument and no
         additional keyword arguments, it attaches itself to the class so it
         gets applied automatically to all test cases found in that class.
      2. If called with a single function as its only positional argument and
         no additional keyword arguments, it attaches a MarkInfo object to the
         function, containing all the arguments already stored internally in
         the MarkDecorator.
      3. When called in any other case, it performs a 'fake construction' call,
         i.e. it returns a new MarkDecorator instance with the original
         MarkDecorator's content updated with the arguments passed to this
         call.

    Note: The rules above prevent MarkDecorator objects from storing only a
    single function or class reference as their positional argument with no
    additional keyword or positional arguments.

    """
    mark = ...
    name = ...
    args = ...
    kwargs = ...
    @property
    def markname(self):
        ...
    
    def __eq__(self, other) -> bool:
        ...
    
    def __repr__(self):
        ...
    
    def with_args(self, *args, **kwargs):
        """ return a MarkDecorator with extra arguments added

        unlike call this can be used even if the sole argument is a callable/class

        :return: MarkDecorator
        """
        ...
    
    def __call__(self, *args, **kwargs):
        """ if passed a single callable argument: decorate it with mark info.
            otherwise add *args/**kwargs in-place to mark information. """
        ...
    


def get_unpacked_marks(obj):
    """
    obtain the unpacked marks that are stored on an object
    """
    ...

def normalize_mark_list(mark_list):
    """
    normalizes marker decorating helpers to mark objects

    :type mark_list: List[Union[Mark, Markdecorator]]
    :rtype: List[Mark]
    """
    ...

def store_mark(obj, mark):
    """store a Mark on an object
    this is used to implement the Mark declarations/decorators correctly
    """
    ...

class MarkGenerator(object):
    """ Factory for :class:`MarkDecorator` objects - exposed as
    a ``pytest.mark`` singleton instance.  Example::

         import pytest
         @pytest.mark.slowtest
         def test_function():
            pass

    will set a 'slowtest' :class:`MarkInfo` object
    on the ``test_function`` object. """
    _config = ...
    _markers = ...
    def __getattr__(self, name):
        ...
    


MARK_GEN = MarkGenerator()
class NodeKeywords(MappingMixin):
    def __init__(self, node) -> None:
        ...
    
    def __getitem__(self, key):
        ...
    
    def __setitem__(self, key, value):
        ...
    
    def __delitem__(self, key):
        ...
    
    def __iter__(self):
        ...
    
    def __len__(self):
        ...
    
    def __repr__(self):
        ...
    


@attr.s(hash=False, **{ ATTRS_EQ_FIELD: False })
class NodeMarkers(object):
    """
    internal structure for storing marks belonging to a node

    ..warning::

        unstable api

    """
    own_markers = ...
    def update(self, add_markers):
        """update the own markers
        """
        ...
    
    def find(self, name):
        """
        find markers in own nodes or parent nodes
        needs a better place
        """
        ...
    
    def __iter__(self):
        ...
    

