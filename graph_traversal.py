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
import phonenumbers

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
        """
        Append to q node upsert statements for element using mapping.

        The query is built by searching node with label mapping.label with
        properties equal to mapping.key_properties.
        If not found a new node with label mapping.label and properties set to
        element's values selected by mapping.key_properties is inserted.
        After the node is upserted every property not belonging to key or to
        relations is set using an optional set clause if mapping.merge_behavior
        is merge_if_not_present or setting unconditionally id merge_behavior is
        merge_always.

        The query is built recursively on mapping.relations and appended to q.
        """
        # Search node by mapping's key properies and label.
        # Node's labels are not indexable the surrogate property lbl is used.
        q = reduce(
            lambda q, property_mapping: q.has(
                property_mapping.name,
                element[property_mapping.source]
            ),
            mapping.key_properties(),
            q.V().has('lbl', mapping.label)
        )
        # This is gremlin's pattern to upserting.
        #
        # Uses coalesce (returns first non null argument) to return either the
        # found node (first argument) or a new node (second argument).
        # The fold-unfold sequence is used to get a null value if node is not
        # found.
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
        # Iterate record's columns searching for property mappings which apply
        # in this context.
        for source_key in element.keys():
            # Get property mapping matching current column by source.
            property_mapping = mapping.property_by_source(source_key)
            if property_mapping is None:
                continue  # Key not mapped in current context
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
                # Assign value to property unconditionally
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
                # Assign value to property if not exists
                q = q.property(
                    property_mapping.name,
                    choose(
                        has(property_mapping.name),
                        values(property_mapping.name),
                        constant(value)
                    )
                )
            else:
                # cml 1 rt text="Unsupported merge beahvior"
                raise Exception('unsupported merge behavior: {}'.format(
                    property_mapping.merge_behavior)
                )
        for relation in mapping.relations:
            # Recursive call on relations
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
        """
        Append to q edge upsert statements for element using mapping.

        The query is built iterating relations by searching for edges with label
        mapping.relations[i].label wich exit from the node identified by mapping
        and enter into the node identified by mapping.relations[i].
        The found edge must also match mapping.relations[i].edge_keys.

        If not found a new edge with label mapping.relations[i].label and
        properties set to mapping.relations[i].edge_keys is inserted.
        The new edge source node will be the one identified from current
        relation and the target node the one identified by the relation.

        After the edge is upserted every property not belonging to edge_keys in
        mapping.relations[i].edge_propertiesis set using an optional set clause
        if mapping.merge_behavior is merge_if_not_present or setting
        unconditionally id merge_behavior is merge_always.

        The query is built recursively on mapping.relations and appended to q.
        """
        if parent is None:
            # Make sure mapping's name is not empty.
            # Tolerates empty name only for root mapping since it doesn't
            # introduce edges.
            if mapping.name.strip() == '':
                relation_name = '_root_mapping'
            else:
                relation_name = mapping.name
            # Generate a reference for later use
            ref = '{}_{}'.format(depth, relation_name)
            # Search node by mapping's key properies and label (uses surrogate
            # property lbl)
            q = reduce(
                lambda q, property_mapping: q.has(
                    property_mapping.name,
                    element[property_mapping.source]
                ),
                mapping.key_properties(),
                q.V().has('lbl', mapping.label)

                # Alias source node usign ref
            ).as_(ref)
        else:
            # Reconstruct references of previous call
            relation_name = '{}_{}'.format(depth, parent.name)
            ref = '{}_{}'.format(depth, relation_name)
        for relation in mapping.relations:
            # Generate target node reference for current relation
            rel_ref = '{}_{}'.format(depth, relation.name)

            # Search target node by relations's key properties and give alias
            # rel_ref
            q = reduce(
                lambda q, property_mapping: q.has(
                    property_mapping.name,
                    element[property_mapping.source]
                ),
                relation.key_properties(),
                q.V().has('lbl', mapping.label)
            ).as_(rel_ref)
            # Search edge matching ref--[relation.name]-->rel_ref and properties
            # matching relation's edge key properties.
            # Insert new edge if not exists and set key properties.
            # This is the same upsert pattern used for nodes adapted for edges
            # (see build_vertex_query).
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
            # Iterate record's columns searching for property mappings which apply
            # in this context.
            for source_key in element.keys():
                property_mapping = mapping.property_by_source(source_key)
                if not property_mapping:
                    continue  # Key not mapped in current context
                if mapping.is_edge_property(relation, property_mapping):
                    if mapping.is_key_property(property_mapping):
                        # cml 1 rt text="Key properties can't be edge property"
                        raise Exception(
                            'key properties cannot be edge properties')
                    if property_mapping.merge_behavior == merge_always:
                        # Assign value uncoditionally
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
                        # Assign if property does not exists
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
                        raise Exception('Unsupported merge behavior: {}'.format(
                            property_mapping.merge_behavior)
                        )
            # Apply recursively
            self.build_edge_query(q, relation, element, depth + 1, mapping)
        # Return built query
        return q

    def build_query(
        self,
        q: graph_traversal.GraphTraversal,
        mapping: Mapping,
        element: Dict[str, Any],
    ) -> graph_traversal.GraphTraversal:
        """
        This is the first version of the query builder.
        It inserts all nodes and edges for current mapping in a single pass.
        The behavior is similar to build_vertex_query and build_edge_query 
        combined.
        """
        # Search for nodes matching label (using surrogate property lbl)
        q = q.V().has('lbl', mapping.label)
        # Search node by mapping.key_properties
        for property_mapping in mapping.key_properties():
            q = q.has(
                property_mapping.name,
                element[property_mapping.source]
            )
        # Build insert clause for later use
        qAddV = addV(mapping.label).property('lbl', mapping.label)
        for property_mapping in mapping.key_properties():
            qAddV = qAddV.property(
                property_mapping.name,
                element[property_mapping.source]
            )
        # Combine search and insert using upsert pattern
        q = q.fold().coalesce(
            unfold(),
            qAddV
        )
        # Search element keys and map on upserted node
        for source_key in element.keys():
            property_mapping = mapping.property_by_source(source_key)
            if property_mapping is None:
                continue  # Key not mapped in current context
            # Check that current property is not an edge property
            if reduce(
                lambda l, r: l or mapping.is_edge_property(
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
                # Assign unconditionally
                q = q.property(
                    property_mapping.name,
                    element[property_mapping.source]
                )
            # cml 1 rt text="property_mapping.merge_behavior == merge_if_not_present"
            elif property_mapping.merge_behavior == merge_if_not_present or property_mapping.merge_behavior == None:
                # Assign if property does not exists
                q = q.property(
                    property_mapping.name,
                    choose(
                        has(property_mapping.name),
                        values(property_mapping.name),
                        constant(
                            element[property_mapping.source]
                        )
                    )
                )
            else:
                # cml 1 rt text="Unsupported merge behavior"
                raise Exception('unsupported merge behavior: {}'.format(
                    property_mapping.merge_behavior)
                )
        # Generate reference to node, using aggregate because `as` aliases are
        # dropped during traversal generated from recursive call.
        mapping_ref = '_{}'.format(mapping.name)
        q = q.aggregate(mapping_ref)
        for relation in mapping.relations:
            # Recursive step
            q = self.build_query(
                q=q,
                mapping=relation,
                element=element,
            )
            rel_ref = '_{}'.format(relation.name)
            edge_keys = mapping.edge_key_properties(relation)
            # Now we build edge upsert pattern
            if edge_keys is None or len(edge_keys) == 0:
                # There are no edge keys.
                # Search relation by source and target nodes.
                q = q.coalesce(
                    select(rel_ref).unfold().inE(relation.name).where(
                        outV().where(P.within(mapping_ref))
                    ),
                    select(mapping_ref).unfold().addE(relation.name).to(
                        select(rel_ref).unfold()
                    )
                )
            else:
                # Build search clause for later use
                s_q = select(rel_ref).unfold().inE(relation.name).where(
                    outV().where(P.within(mapping_ref))
                )
                # Add edge_keys to search clause
                for key in edge_keys:
                    s_q = s_q.where(
                        has(
                            key.name,
                            element[key.source]
                        )
                    )
                # Upsert edge
                q = q.coalesce(
                    s_q,
                    select(mapping_ref).unfold().addE(relation.name).to(
                        select(rel_ref).unfold()
                    )
                )
            # Map relation.edge_properties
            for source_key in element.keys():
                property_mapping = mapping.property_by_source(source_key)
                if not property_mapping:
                    continue  # key not mapped in current context
                if mapping.is_edge_property(relation, property_mapping):
                    if mapping.is_key_property(property_mapping):
                        # cml 1 rt text="Key properties cannot be edge properties"
                        raise Exception(
                            'key properties cannot be edge properties')
                    if property_mapping.merge_behavior == merge_always:
                        # Assign unconditionally
                        q = q.property(
                            property_mapping.name,
                            element[property_mapping.source]
                        )
                    # cml 1 rt text="property_mapping.merge_behavior == merge_if_not_present"
                    elif property_mapping.merge_behavior == merge_if_not_present or property_mapping.merge_behavior == None:
                        # Assign if property does not exists
                        q = q.property(
                            property_mapping.name,
                            choose(
                                has(property_mapping.name),
                                values(property_mapping.name),
                                constant(
                                    element[property_mapping.source]
                                )
                            )
                        )
                    else:
                        # cml 1 rt text="Unsupported merge behavior"
                        raise Exception('unsupported merge behavior: {}'.format(
                            property_mapping.merge_behavior)
                        )
        return q

    def map_data(
        self,
        mapping: Mapping,
        df: pd.DataFrame,
    ) -> None:
        """
        Map's Dataframe's data using mapping.
        """
        def _checkKeys(mapping: Mapping) -> None:
            """
            Sanity check. Mapping's should have at least one key.
            """
            if len(mapping.keys) == 0:
                # cml 1 rt text="The mapping has no keys"
                raise Exception(
                    'mapping <{}> has no keys'.format(mapping.name))
            # cml 1 rt text="mapping has relations"
            if mapping.relations is not None and len(mapping.relations) > 0:
                for m in mapping.relations:
                    _checkKeys(m)

        def _collectProperties(mapping: Mapping) -> List[PropertyMapping]:
            """
            Collect properties recursively
            """
            ps = []
            for property in mapping.properties:
                ps.append(property)
            # cml 1 rt text="mapping has relations"
            if mapping.relations is not None and len(mapping.relations) > 0:
                for m in mapping.relations:
                    ps = ps + _collectProperties(m)
            return ps

        # Use pandas automatic type recognition
        df = df.convert_dtypes()
        # Apply properties' type conversions if specified
        for property in _collectProperties(mapping):
            if property.source not in df.columns:
                continue
            if property.kind == 'datetime':
                df[property.source] = df[property.source].map(parse_date)
            elif property.kind == 'bool':
                def _parseBool(b):
                    if isinstance(b, bool):
                        return b
                    elif isinstance(b, int) or isinstance(b, float):
                        return b != 0
                    elif isinstance(b, str):
                        return b != '0'
                df[property.source] = df[property.source].apply(_parseBool)
            else:
                df[property.source] = df[property.source].astype(property.kind)

            if property.format == 'phone':
                def _map_phone(phone: str) -> str:
                    try:
                        n = phonenumbers.parse(
                            phone, None if phone.startswith('+') else 'IT')
                        if not phonenumbers.is_possible_number(n):
                            return ''
                        return phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.E164)
                    except:
                        return ''
                    # if match is None:
                    #     return ''
                    # v = match.group(0).replace(' ', '').replace('-', '')
                    # if len(v) == 10:
                    #     return "+39" + v
                    # elif v.startswith('39'):
                    #     return "+" + v
                    # return v
                df[property.source] = df[property.source].map(_map_phone)
                df = df[df[property.source] != '']

        data = df.to_dict('records')
        for element in data:
            # Delete keys with null values
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
            """
            Gremlin uses websockets which have a max frame size, so queries 
            can't be of arbitrary size.
            This function calculates the max number of nodes that can be 
            inserted by as single build_vertex_query() call
            """
            if not mapping.relations:
                return 1
            return 1 + sum([_mapping_max_depth(r) for r in mapping.relations])
        # Batch size for nodes.
        # Tuned to be as big as possible without exceeding the frame size.
        batch_size = 15
        max_depth = _mapping_max_depth(mapping)
        loops = math.floor(batch_size / max_depth)

        # Batch insert nodes
        i = 0
        q: graph_traversal.GraphTraversal = self.g
        counter = 0
        for element in tqdm(data):
            q = self.build_vertex_query(q, mapping, element)
            counter = counter + 1
            # At max we mapped batch_size nodes for current query.
            # Trigger insert
            if counter == loops:
                q.next()
                q = self.g
                counter = 0
            i = i + 1
        # Insert eventually remaining nodes
        if counter != 0:
            q.next()

        # Batch insert edges
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
        # Insert remaining edges
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
