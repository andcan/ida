from __future__ import annotations

from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __, outV, select
from data import Mapping, NodeSchema, PropertyMapping, PropertySchema, Schema, merge_always, merge_if_not_present
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple
from gremlin_python.process.graph_traversal import GraphTraversalSource, addV, choose, constant, elementMap, has, local, unfold, valueMap, values, key, label, properties, value
import gremlin_python.process.graph_traversal as graph_traversal
from gremlin_python.process.traversal import Column, P
import pandas as pd
import numpy as np
from data_loader import parse_date, phone_regex
from functools import reduce
import time
from util import format_query

ErrKeyMappingNoCorrespondingPropertyMapping = 'ErrKeyMappingNoCorrespondingPropertyMapping'

ErrSourceKeyNoCorrespondingPropertyMapping = 'ErrSourceKeyNoCorrespondingPropertyMapping'

ErrPropertyMappingNoCorrespondingPropertySchema = 'ErrPropertyMappingNoCorrespondingPropertySchema'


class MappingError(Exception):

    def __init__(self, code: str, args: Optional[Dict[str, Any]] = None):
        self.code = code
        self.arguments = args


class GraphTraversal(object):

    def __init__(self, g: GraphTraversalSource):
        super(GraphTraversal, self).__init__()
        self._g = g

    @staticmethod
    def from_url(url: str, traversal_source: str) -> GraphTraversal:
        return GraphTraversal(traversal().withRemote(DriverRemoteConnection(url, traversal_source)))

    @property
    def g(self) -> GraphTraversalSource:
        return self._g

    def has_duplicates(self, mapping: Mapping) -> bool:
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

    def build_query(
        self,
        q: graph_traversal.GraphTraversal,
        mapping: Mapping,
        element: Dict[str, Any],
    ) -> graph_traversal.GraphTraversal:
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
            if property_mapping is None:
                continue  # key not mapped in current context
            if reduce(
                lambda l, r: l or mapping.is_edge_property(
                    r,
                    property_mapping  # type: ignore
                ),
                mapping.relations,
                False,
            ):
                continue
            if mapping.is_key_property(property_mapping):
                continue
            if property_mapping.merge_behavior == merge_always:
                q = q.property(
                    property_mapping.name,
                    element[property_mapping.source]
                )
            elif property_mapping.merge_behavior == merge_if_not_present or property_mapping.merge_behavior == None:
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
        mapping_ref = '_{}'.format(mapping.name)
        q = q.aggregate(mapping_ref)
        for relation in mapping.relations:
            q = self.build_query(
                q=q,
                mapping=relation,
                element=element,
            )
            rel_ref = '_{}'.format(relation.name)
            edge_keys = mapping.edge_key_properties(relation)
            if edge_keys is None or len(edge_keys) == 0:
                q = q.coalesce(
                    select(rel_ref).unfold().inE(relation.name).where(
                        outV().where(P.within(mapping_ref))
                    ),
                    select(mapping_ref).unfold().addE(relation.name).to(
                        select(rel_ref).unfold()
                    )
                )
            else:
                s_q = select(rel_ref).unfold().inE(relation.name).where(
                    outV().where(P.within(mapping_ref))
                )
                for key in edge_keys:
                    s_q = s_q.where(
                        has(
                            key.name,
                            element[key.source]
                        )
                    )
                q = q.coalesce(
                    s_q,
                    select(mapping_ref).unfold().addE(relation.name).to(
                        select(rel_ref).unfold()
                    )
                )
            for source_key in element.keys():
                property_mapping = mapping.property_by_source(source_key)
                if not property_mapping:
                    continue  # key not mapped in current context
                if mapping.is_edge_property(relation, property_mapping):
                    if mapping.is_key_property(property_mapping):
                        raise Exception(
                            'key properties cannot be edge properties')
                    if property_mapping.merge_behavior == merge_always:
                        q = q.property(
                            property_mapping.name,
                            element[property_mapping.source]
                        )
                    elif property_mapping.merge_behavior == merge_if_not_present or property_mapping.merge_behavior == None:
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
        return q

    def map_data(
        self,
        mapping: Mapping,
        df: pd.DataFrame,
    ) -> None:
        def _checkKeys(mapping: Mapping) -> None:
            if len(mapping.keys) == 0:
                raise Exception(
                    'mapping <{}> has no keys'.format(mapping.name))
            if mapping.relations is not None and len(mapping.relations) > 0:
                for m in mapping.relations:
                    _checkKeys(m)

        def _collectProperties(mapping: Mapping) -> List[PropertyMapping]:
            ps = []
            for property in mapping.properties:
                ps.append(property)
            if mapping.relations is not None and len(mapping.relations) > 0:
                for m in mapping.relations:
                    ps = ps + _collectProperties(m)
            return ps

        df = df.convert_dtypes()
        for property in _collectProperties(mapping):
            if property.source not in df.columns:
                continue
            if property.kind == 'str':
                df[property.source] = df[property.source].astype('str')
            elif property.kind == 'int':
                df[property.source] = df[property.source].astype(
                    np.int64)  # type: ignore
            elif property.kind == 'float':
                df[property.source] = df[property.source].astype(
                    np.float64)  # type: ignore
            elif property.kind == 'datetime':
                df[property.source] = df[property.source].map(parse_date)

            if property.format == 'phone':
                def _map_phone(phone: str) -> str:
                    match = phone_regex.search(phone)
                    if match is None:
                        return ''
                    v = match.group(0).replace(' ', '').replace('-', '')
                    if len(v) == 10:
                        return "+39" + v
                    elif v.startswith('39'):
                        return "+" + v
                    return v
                df[property.source] = df[property.source].map(_map_phone)
                df = df[df[property.source] != '']
        data = df.to_dict('records')
        for element in data:
            # delete keys with null values
            to_delete = []
            for key in element.keys():
                if pd.isnull(element[key]):
                    to_delete.append(key)
                else:
                    try:
                        f = getattr(element[key], 'item')
                        element[key] = f()
                    except AttributeError:
                        pass

            for k in to_delete:
                del element[k]

        print(str(self._g.V().count().next()) + ' nodes')

        rows = len(data)
        i = 0
        last = '0'
        start = time.time()
        for element in data:
            current = str(round(i/rows, 2))
            if current != last:
                print(current + '% (' + str(i) + 'records, + ' +
                      str(time.time() - start) + 's)')
                last = current
            q = self.build_query(
                self._g,  # type: ignore
                mapping,
                element,
            )
            q.next()
            i = i + 1

    def labels(self) -> Sequence[str]:
        return self._g.V().label().dedup().toList()

    def properties(self, label: Optional[str] = None) -> Sequence[str]:
        q = self._g.V()
        if label != None:
            q = q.hasLabel(label)
        q = q.properties().key().dedup()
        return q.toList()

    def remove_all_vertexes(self):
        self._g.V().drop().iterate()

    # TODO: check how to use indexes to make this faster, janus reports:
    # WARN  org.janusgraph.graphdb.transaction.StandardJanusGraphTx  - Query requires iterating over all vertices [()]. For better performance, use indexes
    def schema(self) -> Schema:
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
