from hypothesis.strategies._internal.core import booleans, integers, one_of
from hypothesis.strategies._internal.strategies import SearchStrategy
from graph_traversal import GraphTraversal
from data import KeyMapping, Mapping, NodeSchema, PropertySchema
from typing import Any, Callable, Dict, Optional, Sequence, Tuple, Union
from hypothesis.strategies import composite, lists, sampled_from, text, from_regex, integers, sets, fixed_dictionaries, from_type, floats


@composite  # type: ignore
def property_schemas(draw):
    # type: (Any) -> PropertySchema
    return PropertySchema(
        name=draw(text()),
        kind=draw(sampled_from([
            'Byte',
            'Short',
            'Integer',
            'Long',
            'Float',
            'Double',
            'String',
            'Geoshape',
            'Date',
            'Instant',
            'UUID',
        ])),
    )


@composite  # type: ignore
def node_schemas(draw):
    # type: (Any) -> NodeSchema
    return NodeSchema(
        label=draw(text()),
        properties=draw(lists(property_schemas()))
    )
