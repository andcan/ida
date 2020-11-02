from ida.data import NodeSchema, PropertySchema
from typing import Any
from hypothesis.strategies import composite, lists, sampled_from, text

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
        label = draw(text()),
        properties = draw(lists(property_schemas())) # type: ignore
    )
