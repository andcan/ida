

from .data import NodeSchema, PropertySchema
from typing import Any, Dict, List
from gremlin_python.process.graph_traversal import GraphTraversalSource
from gremlin_python.process.graph_traversal import key, label, properties, value


class GraphTraversal(object):

    def __init__(self, g):
        # type: (GraphTraversalSource) -> None
        super(GraphTraversal, self).__init__()
        self._g = g

    @property
    def g(self):
        # type: () -> GraphTraversalSource
        return self._g

    def nodes_schema(self):
        # type: () -> List[NodeSchema]
        result = self.g.V().group().by(label()).by(
            properties().group().by(key()).by(
                value().map(lambda: ('it.get().getClass()', 'gremlin-groovy'))
            )
        ).next()
        nodes = []  # type: List[NodeSchema]
        for lbl in result.keys():
            node_data = result[lbl]  # type: Dict[str, Any]
            props = []
            for property_name in node_data.keys():
                # type: Dict[str, Any]
                property_data = node_data[property_name]
                property_kind = property_data['@value']  # type: str
                property_kind = property_kind[property_kind.rfind('.') + 1:]
                props.append(PropertySchema(
                    name=property_name,
                    kind=property_kind,
                ))
            nodes.append(NodeSchema(
                label=lbl,
                properties=props,
            ))

        return nodes
