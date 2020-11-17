from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __, outV, select
from data import KeyMapping, Mapping, NodeSchema, PropertySchema, Schema, merge_always, merge_if_not_present
from typing import Any, Dict, List, Optional, Sequence
from gremlin_python.process.graph_traversal import GraphTraversalSource, addV, choose, constant, elementMap, has, local, unfold, valueMap, values, key, label, properties, value
import gremlin_python.process.graph_traversal as graph_traversal
from gremlin_python.process.traversal import Column, P

ErrKeyMappingNoCorrespondingPropertyMapping = 'ErrKeyMappingNoCorrespondingPropertyMapping'

ErrSourceKeyNoCorrespondingPropertyMapping = 'ErrSourceKeyNoCorrespondingPropertyMapping'

ErrPropertyMappingNoCorrespondingPropertySchema = 'ErrPropertyMappingNoCorrespondingPropertySchema'


class MappingError(Exception):

    def __init__(self, code, args=None):
        # type: (str, Optional[Dict[str, Any]]) -> None
        self.code = code
        self.arguments = args


class GraphTraversal(object):

    def __init__(self, g):
        # type: (GraphTraversalSource) -> None
        super(GraphTraversal, self).__init__()
        self._g = g

    @staticmethod
    def from_url(url, traversal_source):
        # type: (str, str) -> GraphTraversal
        return GraphTraversal(traversal().withRemote(DriverRemoteConnection(url, traversal_source)))

    @property
    def g(self):
        # type: () -> GraphTraversalSource
        return self._g

    def has_duplicates(self, mapping):
        # type: (Mapping) -> bool
        keys = list(
            map(
                lambda e: e.name,
                mapping.key_properties(),
            ),
        )
        count = self._g.V().hasLabel(mapping.label).groupCount().by(  # type: Dict[str, Any]
            values(*keys).fold()
        ).select(Column.values).unfold().is_(P.gt(1)).count().next()
        return count > 0

    def build_query_map_vertex(
        self,
        q,  # type: graph_traversal.GraphTraversal
        mapping,  # type: Mapping
        element,  # type: Dict[str, Any]
    ):
        # type: (...) -> graph_traversal.GraphTraversal

        return q

    def build_query(
        self,
        q,  # type: graph_traversal.GraphTraversal
        mapping,  # type: Mapping
        element,  # type: Dict[str, Any]
    ):
        # type: (...) -> graph_traversal.GraphTraversal
        q = q.V().hasLabel(mapping.label)
        for property_mapping in mapping.key_properties():
            q = q.has(
                property_mapping.name,
                element[property_mapping.source]
            )

        qAddV = addV(mapping.label)
        for property_mapping in mapping.key_properties():
            qAddV = qAddV.property(
                property_mapping.name,
                element[property_mapping.source]
            )

        q = q.fold().coalesce(
            unfold(),
            qAddV
        )
        for source_key in element.keys():
            property_mapping = mapping.property_by_source(source_key)
            if not property_mapping:
                continue  # key not mapped in current context
            if mapping.is_key_property(property_mapping):
                continue
            if property_mapping.merge_behavior == merge_always:
                q = q.property(
                    property_mapping.name,
                    element[property_mapping.source]
                )
            elif property_mapping.merge_behavior == merge_if_not_present:
                q = q.property(
                    property_mapping.name,
                    choose(
                        has(property_mapping.name),
                        values(property_mapping.name),
                        constant(element[property_mapping.source])
                    )
                )
            else:
                raise Exception('unsupported merge behavior: {}'.format(
                    property_mapping.merge_behavior)
                )
        hasRelations = mapping.relations != None and len(
            mapping.relations) != 0
        mapping_ref = '_{}'.format(mapping.name)
        if hasRelations:
            q = q.aggregate(mapping_ref)
        for relation in mapping.relations:
            q = self.build_query(
                q=q,
                mapping=relation,
                element=element,
            )
            rel_ref = '_{}'.format(relation.name)
            q = q.coalesce(
                select(rel_ref).unfold().inE(relation.name).where(
                    outV().where(P.within(mapping_ref)),
                    select(mapping_ref).unfold().addE(relation.name).to(
                        select(rel_ref).unfold()
                    )
                )
            )
        return q

    def map_data(
        self,
        mapping,  # type: Mapping
        data,  # type: Sequence[Dict[str, Any]]
    ):
        for element in data:
            q = self.build_query(
                self._g,
                mapping,
                element,
            )
            q = self._g.V().hasLabel(mapping.label)
            qAddV = addV(mapping.label)
            for property_mapping in mapping.key_properties():
                q = q.has(property_mapping.name,
                          element[property_mapping.source])
                qAddV = qAddV.property(
                    property_mapping.name,
                    element[property_mapping.source]
                )

            q = q.fold().coalesce(
                unfold(),
                qAddV,
            )
            for source_key in element.keys():
                property_mapping = mapping.property_by_source(source_key)
                if not property_mapping:
                    continue  # key not mapped in current context
                    # raise MappingError(
                    #     ErrSourceKeyNoCorrespondingPropertyMapping,
                    #     args={'source': source_key},
                    # )
                if mapping.is_key_property(property_mapping):
                    continue
                if property_mapping.merge_behavior == merge_always:
                    q = q.property(property_mapping.name,
                                   element[property_mapping.source])
                elif property_mapping.merge_behavior == merge_if_not_present:
                    q = q.property(
                        property_mapping.name,
                        choose(
                            has(property_mapping.name),
                            values(property_mapping.name),
                            constant(element[property_mapping.source])
                        )
                    )
                else:
                    raise Exception('unsupported merge behavior: {}'.format(
                        property_mapping.merge_behavior))
            q.next()

    def labels(self):
        # type: () -> Sequence[str]
        return self._g.V().label().dedup().toList()

    def properties(self, label=None):
        # type: (Optional[str]) -> Sequence[str]
        q = self._g.V()
        if label != None:
            q = q.hasLabel(label)
        q = q.properties().key().dedup()
        return q.toList()

    def remove_all_vertexes(self):
        self._g.V().drop().iterate()

    # TODO: check how to use indexes to make this faster, janus reports:
    # WARN  org.janusgraph.graphdb.transaction.StandardJanusGraphTx  - Query requires iterating over all vertices [()]. For better performance, use indexes
    def schema(self):
        # type: () -> Schema
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

        return Schema(nodes=nodes)
