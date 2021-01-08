"""
This type stub file was generated by pyright.
"""

class OperatorTypes(object):
    """
    OperatorTypes is used as struct to store the operator types flags.
    """
    ATTRIBUTE = ...
    ACCESSOR = ...
    MATCHER = ...


class Operator(object):
    """
    Operator implements a base class with common logic and required interface
    that is used by specific operator implementations.

    Any operator should inherit from this class.

    Attributes:
        Dsl (grappa.operators_dsl): DSL for operator error messages templating
        Type (grappa.operators.OperatorTypes): support operators types
        kind (str): stores the operator kind
        operators (list|tuple): operator keywords
        aliases (list|tuple): chain attributes aliases for expressivity
        information (list|tuple): optional additional help in case of error
        subject_message (str|Operator.Dsl.Message): optional subject message
        expected_message (str|Operator.Dsl.Message): optional expected message
        operator_name (str): invokation operator name keyword
        suboperators (list|tuple[grappa.Operator]): optional child operators
    """
    Dsl = ...
    Type = ...
    kind = ...
    operators = ...
    aliases = ...
    chainable = ...
    information = ...
    ctx = ...
    operator_name = ...
    suboperators = ...
    value = ...
    expected = ...
    subject_message = ...
    expected_message = ...
    def __init__(self, context=..., operator_name=..., fn=..., kind=..., aliases=..., operators=..., suboperators=...) -> None:
        ...
    
    def match(self, *args, **kw):
        ...
    
    def __call__(self, *args, **kw):
        """
        Overloads function invokation in current operator and creates a new
        cloned operator instance.
        """
        ...
    
    def observe(matcher):
        """
        Internal decorator to trigger operator hooks before/after
        matcher execution.
        """
        ...
    
    @observe
    def run_matcher(self, subject, *expected, **kw):
        """
        Runs the operator matcher test function.
        """
        ...
    
    def run(self, *args, **kw):
        """
        Runs the current operator with the subject arguments to test.

        This method is implemented by matchers only.
        """
        ...
    
    def __enter__(self):
        ...
    
    def __exit__(self, etype, value, traceback):
        ...
    

