"""
This type stub file was generated by pyright.
"""

from typing import Callable
from .base import BaseTest


class Test(BaseTest):
    """
    Test represents the test definition in `grappa` with extensible and
    dynamic, runtime inferred DSL based on registered operators and
    third-party plugins.

    Arguments:
        subject (mixed): subject value to test.
    """
    _context = ...
    _context_subject = ...
    _global = ...

    def __init__(self, subject=...) -> None:
        ...

    @property
    def should(self):
        """
        Alias name to self reference the current instance.
        Required for DSL API.
        """
        ...

    @property
    def expect(self):
        """
        Alias name to self reference the current instance.
        Required for DSL API.
        """
        ...

    def __call__(self, subject, overload=...):
        """
        Overloads function invokation of `Test` class instance.

        This is magical and widely used in `grappa` test execution by both
        developers and internal engine.

        Arguments:
            subject (mixed): test subject to use.
            overload (bool): `True` if the call if triggered via operator
                overloading invokation, otherise `False`.

        Returns:
            grappa.Test: new test instance with the given subject.
        """
        ...

    def __getattr__(self, name):
        """
        Overloads class attribute accessor proxying calls dynamically
        into assertion operators calls.

        This method is invoked by Python runtime engine, not by developers.
        """
        ...

    def all(self, *tests):
        """
        Composes multiple tests and executes them, in series, once a
        subject is received.

        Conditional composition operator equivalent to `all` built-in
        Python function.

        Arguments:
            *tests (grappa.Test): test instances to run.
        """
        ...

    def any(self, *tests):
        """
        Composes multiple tests and executes them, in series, once a
        subject is received.

        Conditional composition operator equivalent to `any` built-in
        Python function.

        Arguments:
            *tests (grappa.Test): test instances to run.
        """
        ...

    def __overload__(self, subject):
        """
        Method triggered by magic methods executed via operator overloading.
        """
        ...

    def __or__(self, value):
        """
        Overloads ``|`` as from left-to-right operator precedence expression.
        """
        ...

    def __ror__(self, value):
        """
        Overloads ``|`` operator.
        """
        ...

    def __gt__(self, value) -> bool:
        """
        Overloads ``>`` operator.
        """
        ...

    def __enter__(self):
        """
        Initializes context manager.
        """
        ...

    def __exit__(self, etype, value, traceback):
        """
        Exists context manager.
        """
        ...

    @property
    def equal(self) -> Test:
        ...

    @property
    def to(self) -> Callable[..., Test]:
        ...

    @property
    def true(self) -> Test:
        ...


test = Test()
