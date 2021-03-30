from __future__ import annotations

from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __, addE, inV, outE, outV, select
from data import Mapping, NodeSchema, PropertyMapping, PropertySchema, Schema, merge_always, merge_if_not_present
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple
from gremlin_python.process.graph_traversal import GraphTraversalSource, addV, choose, constant, elementMap, has, local, unfold, valueMap, values, key, label, properties, value
import gremlin_python.process.graph_traversal as graph_traversal
from gremlin_python.process.traversal import Column, P
import pandas as pd
import numpy as np
from data_loader import parse_date, phone_regex
from functools import reduce
from util import format_query
import math
import time
from tqdm import tqdm

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
        count = self._g.V().has('lbl', mapping.label).groupCount().by(  # type: Dict[str, Any]
            values(*keys).fold()
        ).select(Column.values).unfold().is_(P.gt(1)).count().next()
        return count > 0

    def build_vertex_query(
        self,
        q: graph_traversal.GraphTraversal,
        mapping: Mapping,
        element: Dict[str, Any]
    ) -> graph_traversal.GraphTraversal:
        # search node by mapping's key properies and label
        q = reduce(
            lambda q, property_mapping: q.has(
                property_mapping.name,
                element[property_mapping.source]
            ),
            mapping.key_properties(),
            q.V().has('lbl', mapping.label)
        )
        # gremlin's pattern to for upsert.
        # returns previous node if found or creates a new one usign mapping's
        # key properties
        q = q.fold().coalesce(
            unfold(),
            reduce(
                lambda q, property_mapping: q.property(
                    property_mapping.name,
                    element[property_mapping.source]
                ),
                mapping.key_properties(),
                addV(mapping.label).property('lbl', mapping.label),
            )
        )
        # iterate record columns
        for source_key in element.keys():
            # get property mapping matching current column
            property_mapping = mapping.property_by_source(source_key)
            if property_mapping is None:
                continue  # key not mapped in current context
            # cml 1 rt text="property is any relation's edge property"
            if reduce(
                lambda is_edge_poperty, r: is_edge_poperty or mapping.is_edge_property(
                    r,
                    property_mapping
                ),
                mapping.relations,
                False,
            ):
                continue
            if mapping.is_key_property(property_mapping):
                continue
            if property_mapping.merge_behavior == merge_always:
                # assign value to property
                q = q.property(
                    property_mapping.name,
                    element[property_mapping.source]
                )
            # cml 1 rt text="property_mapping.merge_behavior == merge_if_not_present"
            elif property_mapping.merge_behavior == merge_if_not_present or property_mapping.merge_behavior == None:
                value = element[property_mapping.source]
                # cml 1 rt text="value is null or empty"
                if value is None or value == '<NA>':
                    continue
                # assign value to property if not exists
                q = q.property(
                    property_mapping.name,
                    choose(
                        has(property_mapping.name),
                        values(property_mapping.name),
                        constant(value)
                    )
                )
            else:
                # cml 1 rt text="unsupported merge beahvior"
                raise Exception('unsupported merge behavior: {}'.format(
                    property_mapping.merge_behavior)
                )
        for relation in mapping.relations:
            # apply recursively on relations
            q = self.build_vertex_query(
                q=q,
                mapping=relation,
                element=element,
            )
        return q

    def build_edge_query(
        self,
        q: graph_traversal.GraphTraversal,
        mapping: Mapping,
        element: Dict[str, Any],
        depth=0,
        parent: Optional[Mapping] = None,
    ) -> graph_traversal.GraphTraversal:
        if parent is None:
            # make sure mapping's name is not empty
            # empty name is allowed only for root mapping
            if mapping.name.strip() == '':
                relation_name = '_root_mapping'
            else:
                relation_name = mapping.name
            # generate a reference
            ref = '{}_{}'.format(depth, relation_name)
            # search node by mapping's key properies and label
            q = reduce(
                lambda q, property_mapping: q.has(
                    property_mapping.name,
                    element[property_mapping.source]
                ),
                mapping.key_properties(),
                q.V().has('lbl', mapping.label)
            # alias node usign ref
            ).as_(ref)
        else:
            # reconstruct references of previous iteration
            relation_name = '{}_{}'.format(depth, parent.name)
            ref = '{}_{}'.format(depth, relation_name)
        for relation in mapping.relations:
            # generate node reference for current relation
            rel_ref = '{}_{}'.format(depth, relation.name)
            # search node by relations's key properties 
            q = reduce(
                lambda q, property_mapping: q.has(
                    property_mapping.name,
                    element[property_mapping.source]
                ),
                relation.key_properties(),
                q.V().has('lbl', mapping.label)
                # alias node usign rel_ref
            ).as_(rel_ref)
            # search edge matching ref--[relation.name]-->rel_ref
            # and properties matching relation's edge key properties.
            # insert new edge if not exists and set key properties
            edge_keys = mapping.edge_key_properties(relation)
            q = q.select(ref).coalesce(
                reduce(
                    lambda q, property_mapping: q.has(
                        property_mapping.name,
                        element[property_mapping.source],
                    ),
                    edge_keys,
                    outE('chiamato').where(
                        reduce(
                            lambda q, key: q.has(
                                key.name,
                                element[key.source],
                            ),
                            relation.key_properties(),
                            inV().has('lbl', mapping.label),
                        )
                    )
                ),
                reduce(
                    lambda q, key: q.property(
                        key.name,
                        element[key.source],
                    ),
                    edge_keys,
                    addE(relation.name).from_(select(ref)).to(rel_ref)
                )
            )
            for source_key in element.keys():
                property_mapping = mapping.property_by_source(source_key)
                if not property_mapping:
                    continue  # key not mapped in current context
                if mapping.is_edge_property(relation, property_mapping):
                    if mapping.is_key_property(property_mapping):
                        # cml 1 rt text="key properties can't be edge property"
                        raise Exception(
                            'key properties cannot be edge properties')
                    if property_mapping.merge_behavior == merge_always:
                        # assign value to property
                        q = q.property(
                            property_mapping.name,
                            element[property_mapping.source]
                        )
                    # cml 1 rt text="property_mapping.merge_behavior == merge_if_not_present"
                    elif property_mapping.merge_behavior == merge_if_not_present or property_mapping.merge_behavior == None:
                        value = element[property_mapping.source]
                        # cml 1 rt text="value is null or empty"
                        if value is None or value == '<NA>':
                            continue
                        # assign value to property if not exists
                        q = q.property(
                            property_mapping.name,
                            choose(
                                has(property_mapping.name),
                                values(property_mapping.name),
                                constant(value)
                            )
                        )
                    else:
                        # cml 1 rt text="unsupported merge behavior"
                        raise Exception('unsupported merge behavior: {}'.format(
                            property_mapping.merge_behavior)
                        )
            # apply recursively
            self.build_edge_query(q, relation, element, depth + 1, mapping)
        # return built query
        return q

    def build_query(
        self,
        q: graph_traversal.GraphTraversal,
        mapping: Mapping,
        element: Dict[str, Any],
    ) -> graph_traversal.GraphTraversal:
        q = q.V().has('lbl', mapping.label)
        for property_mapping in mapping.key_properties():
            q = q.has(
                property_mapping.name,
                element[property_mapping.source]
            )

        qAddV = addV(mapping.label).property('lbl', mapping.label)
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

        # rows = len(data)
        # i = 0
        # last = 0
        # start = time.time()
        # for element in data:
        #     current = int(i/rows*100)
        #     if current != last:
        #         timediff = time.time() - start
        #         print(str(current) + '% (' + str(i) + 'records, + ' +
        #               str(timediff) + 's)')
        #         last = current
        #     q = self.build_vertex_query(
        #         self._g,  # type: ignore
        #         mapping,
        #         element,
        #     )
        #     print(format_query(q))
        #     raise Exception(format_query(q))
        #     try:
        #         q.next()
        #     except:
        #         # print(format_query(q))
        #         raise
        #     i = i + 1
        def _mapping_max_depth(mapping: Mapping) -> int:
            if not mapping.relations:
                return 1
            return 1 + sum([_mapping_max_depth(r) for r in mapping.relations])
        batch_size = 15
        max_depth = _mapping_max_depth(mapping)
        loops = math.floor(batch_size / max_depth)

        i = 0
        q: graph_traversal.GraphTraversal = self.g
        counter = 0
        for element in tqdm(data):
            q = self.build_vertex_query(q, mapping, element)
            counter = counter + 1
            if counter == loops:
                q.next()
                q = self.g
                counter = 0
            i = i + 1
        if counter != 0:
            q.next()

        batch_size = 8
        loops = max(math.floor(batch_size / max_depth), 1)

        i = 0
        q: graph_traversal.GraphTraversal = self.g
        counter = 0
        for element in tqdm(data):
            q = self.build_edge_query(q, mapping, element)
            counter = counter + 1
            if counter == loops:
                q.next()
                q = self.g
                counter = 0
            i = i + 1
        if counter != 0:
            q.next()

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
