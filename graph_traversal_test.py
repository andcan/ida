
from data_loader import DataLoader
from gremlin_python.process.graph_traversal import unfold
from data import NodeSchema, PropertySchema, merge_always, merge_if_not_present
from .graph_client import GraphClient
from .graph_traversal import GraphTraversal
from uuid import uuid4
from .graph_traversal import GraphTraversal
from hypothesis.strategies._internal.strategies import SearchStrategy
from .data import KeyMapping, Mapping, PropertyMapping
from typing import Any, Callable, Dict, Iterable, List, Set, Tuple
from .graph_client import GraphClient
import hypothesis.strategies as st
from grappa import should
from funcy.colls import merge
import string
from faker import Faker
from functools import reduce

fake = Faker()


def test_node_info(graph_client, gremlin_url, graph_name):
    # type: (GraphClient, str, str) -> None
    graph_name = 'graph_of_the_gods_' + graph_name
    graph_client.load_graph_of_the_gods(graph_name, create=True)
    gt = GraphTraversal.from_url(
        gremlin_url, '{0}_traversal'.format(graph_name))
    schema = gt.schema()

    nodes = list(
        map(lambda e: e.to_dict(), schema.nodes)
    )
    expected = NodeSchema(
        label='monster',
        properties=[
            PropertySchema(name='name', kind='String'),
        ],
    )
    expected.to_dict() in nodes | should.be.true

    expected = NodeSchema(
        label='god',
        properties=[
            PropertySchema(name='age', kind='Integer'),
            PropertySchema(name='name', kind='String'),
        ])
    expected.to_dict() in nodes | should.be.true

    expected = NodeSchema(
        label='titan',
        properties=[
            PropertySchema(name='age', kind='Integer'),
            PropertySchema(name='name', kind='String'),
        ])
    expected.to_dict() in nodes | should.be.true

    expected = NodeSchema(
        label='demigod',
        properties=[
            PropertySchema(name='age', kind='Integer'),
            PropertySchema(name='name', kind='String'),
        ])
    expected.to_dict() in nodes | should.be.true

    expected = NodeSchema(
        label='human',
        properties=[
            PropertySchema(name='age', kind='Integer'),
            PropertySchema(name='name', kind='String'),
        ])
    expected.to_dict() in nodes | should.be.true

    expected = NodeSchema(
        label='location',
        properties=[
            PropertySchema(name='name', kind='String'),
        ])
    expected.to_dict() in nodes | should.be.true

    gt.remove_all_vertexes()


@st.composite
def property_schemas(
    draw,
    name=st.text(
        alphabet=string.ascii_letters,
        min_size=1,
    ),
    kind=st.sampled_from([
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
    ]),
):
    # type: (Callable[..., Any], SearchStrategy, SearchStrategy) -> PropertySchema
    return PropertySchema(
        name=draw(name),
        kind=draw(kind),
    )


@st.composite
def node_schemas(
    draw,
    label=st.text(
        alphabet=string.ascii_letters,
        min_size=1,
    ),
    properties=st.lists(
        property_schemas(),  # type: ignore
        min_size=2,
        max_size=10,
        unique_by=lambda x: x.name,
    ),
):
    # type: (Callable[..., Any], SearchStrategy, SearchStrategy) -> NodeSchema
    return NodeSchema(
        label=draw(label),
        properties=draw(properties),
    )


@st.composite
def property_mappings(
    draw,
    name=st.text(
        alphabet=string.ascii_letters,
        min_size=1,
    ),
    source=st.text(
        alphabet=string.ascii_letters,
        min_size=1,
    ),
):
    # type: (Callable[..., Any], SearchStrategy, SearchStrategy) -> PropertyMapping
    return PropertyMapping(
        name=draw(name),
        source=draw(source),
    )


@st.composite
def mappings(
    draw,
):
    # type: (...) -> Mapping

    properties = draw(
        st.lists(
            property_mappings(),  # type: ignore
            min_size=2,
            unique_by=(lambda e: e.name, lambda e: e.source)
        )
    )
    key_properties_count = draw(
        st.integers(
            min_value=1,
            max_value=len(properties) - 1,
        )
    )

    return Mapping(
        label=draw(
            st.text(
                alphabet=string.ascii_letters,
                min_size=1,
            ),
        ),
        name='mapping',
        keys=list(
            map(
                lambda e: KeyMapping(
                    name=e.name
                ),
                properties[0:key_properties_count],
            )
        ),
        properties=properties,
        relations=[],
    )


@st.composite
def gen_data(
    draw,
    mapping,
    min_size=1,
):
    # type: (Callable[..., Any], Mapping, int) -> Dict[str, Any]
    property_names = list(
        map(
            lambda e: e.source,
            mapping.properties,
        )
    )
    kinds_dict = draw(
        st.fixed_dictionaries({
            key: st.sampled_from(['str', 'int', 'float', 'bool']) for key in property_names
        })
    )

    def _kind_to_strategy(kind):
        # type: (str) -> SearchStrategy
        if kind == 'str':
            return st.text(
                alphabet=string.ascii_letters,
                min_size=1,
            )
        if kind == 'int':
            return st.integers(
                min_value=0-2147483648,
                max_value=2147483647,
            )
        if kind == 'float':
            return st.floats()
        if kind == 'bool':
            return st.booleans()
        raise Exception('unsupported kind ' + kind)

    strategy_dict = {
        key: _kind_to_strategy(kinds_dict[key]) for key in kinds_dict.keys()
    }
    return draw(
        st.lists(
            st.fixed_dictionaries(strategy_dict),
            min_size=min_size,
        )
    )


# @st.composite
# def mapping__data(
#     draw,  # type: Callable[..., Any]
#     gt,  # type: GraphTraversal
#     label,  # type: str
#     keys,  # type: Sequence[str]
# ):
#     # type: (...) -> Tuple[DataMapping, Sequence[Dict[str, Any]]]
#     properties = gt.properties(label=label)

#     key_values = reduce(
#         lambda g, key_name: g.values(key_name),
#         keys,
#         gt.g.V().hasLabel(label)
#     ).toList()
#     new_properties = draw(
#         st.lists(
#             st.from_regex(r'[A-Za-z][A-Za-z_]*', fullmatch=True),
#             unique=True,
#             min_size=1,
#         ).filter(lambda e: e not in properties)
#     )

#     kinds_dict = draw(
#         st.fixed_dictionaries({
#             k: st.sampled_from(['str', 'int', 'float', 'bool']) for k in new_properties
#         })
#     )

#     def _kind_to_strategy(kind):
#         # type: (str) -> SearchStrategy
#         if kind == 'str':
#             return st.from_regex(r'\w+', fullmatch=True)
#         if kind == 'int':
#             return st.integers(
#                 min_value=0-2147483648,
#                 max_value=2147483647,
#             )
#         if kind == 'float':
#             return st.floats()
#         if kind == 'bool':
#             return st.booleans()
#         raise Exception('unsupported kind ' + kind)

#     strategy_dict = {}  # type: Dict[str, Any]
#     strategy_dict = merge(  # type: ignore
#         {
#             key: _kind_to_strategy(kinds_dict[key]) for key in kinds_dict.keys()
#         },
#         {
#             'name': st.sampled_from(key_values)
#         }
#     )

#     return (
#         DataMapping(
#             label=label,
#             keys=map(lambda e: KeyMapping(name=e), keys),
#             properties=merge(
#                 list(
#                     map(
#                         lambda e: PropertyMapping(
#                             name=e,
#                             source=e,
#                         ),
#                         strategy_dict.keys(),
#                     )
#                 ),
#                 [
#                     PropertyMapping(
#                         name='name',
#                         source='name'
#                     )
#                 ]
#             )
#         ),
#         draw(
#             st.lists(
#                 st.fixed_dictionaries(strategy_dict),
#                 min_size=1,
#             )
#         )
#     )

def test_has_duplicates_simple_key(
        graph_client,  # type: GraphClient
        gremlin_url,  # type: str
):
    graph_name = str(uuid4()).replace('-', '')
    graph_client.create_graph(graph_name)
    graph_client.setup_traversal(graph_name)
    gt = GraphTraversal.from_url(
        gremlin_url,
        '{0}_traversal'.format(graph_name)
    )

    mapping = Mapping(
        label='Person',
        name='mapping',
        keys=[
            KeyMapping(
                name='identifier'
            )
        ],
        properties=[
            PropertyMapping(
                name='identifier',
                source='ID',
            ),
            PropertyMapping(
                name='firstName',
                source='first_name',
                merge_behavior=merge_always,
            ),
            PropertyMapping(
                name='lastName',
                source='last_name',
                merge_behavior=merge_always,
            ),
        ],
        relations=[],
    )
    data = [
        {
            'ID': fake.ssn(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        } for i in range(1, 10)
    ]
    gt.map_data(mapping=mapping, data=data)
    gt.has_duplicates(mapping) | should.be.false

    gt.g.addV(mapping.label).property(
        'identifier', data[0]['ID']
    ).property(
        'firstName', fake.first_name()
    ).property(
        'lastName', fake.last_name()
    ).next()
    gt.has_duplicates(mapping) | should.be.true

    # cleanup
    gt.remove_all_vertexes()


def test_has_duplicates_composite_key(
        graph_client,  # type: GraphClient
        gremlin_url,  # type: str
):
    graph_name = str(uuid4()).replace('-', '')
    graph_client.create_graph(graph_name)
    graph_client.setup_traversal(graph_name)
    gt = GraphTraversal.from_url(
        gremlin_url,
        '{0}_traversal'.format(graph_name)
    )

    mapping = Mapping(
        label='Person',
        name='mapping',
        keys=[
            KeyMapping(
                name='firstName'
            ),
            KeyMapping(
                name='lastName',
            ),
        ],
        properties=[
            PropertyMapping(
                name='identifier',
                source='ID',
                merge_behavior=merge_always,
            ),
            PropertyMapping(
                name='firstName',
                source='first_name',
            ),
            PropertyMapping(
                name='lastName',
                source='last_name',
            ),
        ],
        relations=[]
    )
    data = [
        {
            'ID': fake.ssn(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        } for i in range(1, 10)
    ]
    gt.map_data(mapping=mapping, data=data)
    gt.has_duplicates(mapping) | should.be.false

    gt.g.addV(mapping.label).property(
        'identifier', fake.ssn()
    ).property(
        'firstName', data[0]['first_name']
    ).property(
        'lastName', data[0]['last_name']
    ).next()
    gt.has_duplicates(mapping) | should.be.true

    # cleanup
    gt.remove_all_vertexes()


def test_map_add_new_nodes(
    graph_client,  # type: GraphClient
    gremlin_url,  # type: str
):
    graph_name = str(uuid4()).replace('-', '')
    graph_client.create_graph(graph_name)
    graph_client.setup_traversal(graph_name)
    gt = GraphTraversal.from_url(
        gremlin_url,
        '{0}_traversal'.format(graph_name)
    )

    mapping = Mapping(
        label='Person',
        name='mapping',
        keys=[
            KeyMapping(
                name='identifier'
            )
        ],
        properties=[
            PropertyMapping(
                name='identifier',
                source='ID',
            ),
            PropertyMapping(
                name='firstName',
                source='first_name',
                merge_behavior=merge_always,
            ),
            PropertyMapping(
                name='lastName',
                source='last_name',
                merge_behavior=merge_always,
            ),
        ],
        relations=[],
    )

    data = [
        {
            'ID': fake.ssn(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        } for i in range(1, 10)
    ]

    gt.map_data(mapping=mapping, data=data)

    node_count = gt.g.V().hasLabel(mapping.label).count().next()
    node_count | should.be.equal.to(len(data))

    for d in data:
        count = gt.g.V().hasLabel(mapping.label). \
            has('identifier', d['ID']). \
            has('firstName', d['first_name']). \
            has('lastName', d['last_name']). \
            count(). \
            next()
        count | should.be.equal.to(1)


def test_map_update_nodes(
    graph_client,  # type: GraphClient
    gremlin_url,  # type: str
):
    graph_name = str(uuid4()).replace('-', '')
    graph_client.create_graph(graph_name)
    graph_client.setup_traversal(graph_name)
    gt = GraphTraversal.from_url(
        gremlin_url,
        '{0}_traversal'.format(graph_name)
    )

    mapping = Mapping(
        label='Person',
        name='mapping',
        keys=[
            KeyMapping(
                name='identifier'
            )
        ],
        properties=[
            PropertyMapping(
                name='identifier',
                source='ID',
            ),
            PropertyMapping(
                name='firstName',
                source='first_name',
                merge_behavior=merge_always,
            ),
            PropertyMapping(
                name='lastName',
                source='last_name',
                merge_behavior=merge_always,
            ),
        ],
        relations=[],
    )

    data = [
        {
            'ID': fake.ssn(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        } for i in range(1, 10)
    ]

    gt.map_data(mapping=mapping, data=data)

    new_data = list(
        map(
            lambda e: {
                'ID': e['ID'],
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
            },
            data,
        )
    )
    gt.map_data(mapping=mapping, data=new_data)

    node_count = gt.g.V().hasLabel(mapping.label).count().next()
    node_count | should.be.equal.to(len(data))

    for d in data:
        count = gt.g.V().hasLabel(mapping.label). \
            has('identifier', d['ID']). \
            has('firstName', d['first_name']). \
            has('lastName', d['last_name']). \
            count(). \
            next()
        count | should.be.equal.to(0)

    for d in new_data:
        count = gt.g.V().hasLabel(mapping.label). \
            has('identifier', d['ID']). \
            has('firstName', d['first_name']). \
            has('lastName', d['last_name']). \
            count(). \
            next()
        count | should.be.equal.to(1)


def test_map_add_and_update_nodes(
    graph_client,  # type: GraphClient
    gremlin_url,  # type: str
):
    graph_name = str(uuid4()).replace('-', '')
    graph_client.create_graph(graph_name)
    graph_client.setup_traversal(graph_name)
    gt = GraphTraversal.from_url(
        gremlin_url,
        '{0}_traversal'.format(graph_name)
    )

    mapping = Mapping(
        label='Person',
        name='mapping',
        keys=[
            KeyMapping(
                name='identifier'
            )
        ],
        properties=[
            PropertyMapping(
                name='identifier',
                source='ID',
            ),
            PropertyMapping(
                name='firstName',
                source='first_name',
                merge_behavior=merge_always,
            ),
            PropertyMapping(
                name='lastName',
                source='last_name',
                merge_behavior=merge_always,
            ),
        ],
        relations=[],
    )

    data = [
        {
            'ID': fake.ssn(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        } for i in range(1, 10)
    ]

    gt.map_data(mapping=mapping, data=data)

    overwrite_data = list(
        map(
            lambda e: {
                'ID': e['ID'],
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
            },
            data[0:5],
        )
    )
    new_data = list(
        {
            'ID': fake.ssn(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        } for i in range(1, 10)
    )
    gt.map_data(mapping=mapping, data=merge(overwrite_data, new_data))

    node_count = gt.g.V().hasLabel(mapping.label).count().next()
    node_count | should.be.equal.to(len(data) + len(new_data))

    for i in range(0, len(overwrite_data)):
        d = data[i]
        count = gt.g.V().hasLabel(mapping.label). \
            has('identifier', d['ID']). \
            has('firstName', d['first_name']). \
            has('lastName', d['last_name']). \
            count(). \
            next()
        count | should.be.equal.to(0)

        d = overwrite_data[i]
        count = gt.g.V().hasLabel(mapping.label). \
            has('identifier', d['ID']). \
            has('firstName', d['first_name']). \
            has('lastName', d['last_name']). \
            count(). \
            next()
        count | should.be.equal.to(1)

    for i in range(len(overwrite_data), len(data)):
        d = data[i]
        count = gt.g.V().hasLabel(mapping.label). \
            has('identifier', d['ID']). \
            has('firstName', d['first_name']). \
            has('lastName', d['last_name']). \
            count(). \
            next()
        count | should.be.equal.to(1)

    for d in new_data:
        count = gt.g.V().hasLabel(mapping.label). \
            has('identifier', d['ID']). \
            has('firstName', d['first_name']). \
            has('lastName', d['last_name']). \
            count(). \
            next()
        count | should.be.equal.to(1)


def test_map_update_if_not_present(
    graph_client,  # type: GraphClient
    gremlin_url,  # type: str
):
    graph_name = str(uuid4()).replace('-', '')
    graph_client.create_graph(graph_name)
    graph_client.setup_traversal(graph_name)
    gt = GraphTraversal.from_url(
        gremlin_url,
        '{0}_traversal'.format(graph_name)
    )

    mapping = Mapping(
        label='Person',
        name='mapping',
        keys=[
            KeyMapping(
                name='identifier'
            )
        ],
        properties=[
            PropertyMapping(
                name='identifier',
                source='ID',
            ),
            PropertyMapping(
                name='firstName',
                source='first_name',
                merge_behavior=merge_always,
            ),
            PropertyMapping(
                name='lastName',
                source='last_name',
                merge_behavior=merge_if_not_present,
            ),
        ],
        relations=[],
    )

    data = [
        {
            'ID': fake.ssn(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
        } for i in range(1, 10)
    ]

    gt.map_data(mapping=mapping, data=data)

    new_data = list(
        map(
            lambda e: {
                'ID': e['ID'],
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
            },
            data,
        )
    )
    gt.map_data(mapping=mapping, data=new_data)

    node_count = gt.g.V().hasLabel(mapping.label).count().next()
    node_count | should.be.equal.to(len(data))

    for i in range(0, len(data)):
        d = data[i]
        count = gt.g.V().hasLabel(mapping.label). \
            has('identifier', d['ID']). \
            has('firstName', d['first_name']). \
            has('lastName', d['last_name']). \
            count(). \
            next()
        count | should.be.equal.to(0)

        nd = new_data[i]
        count = gt.g.V().hasLabel(mapping.label). \
            has('identifier', nd['ID']). \
            has('firstName', nd['first_name']). \
            has('lastName', nd['last_name']). \
            count(). \
            next()
        count | should.be.equal.to(0)

        count = gt.g.V().hasLabel(mapping.label). \
            has('identifier', nd['ID']). \
            has('firstName', nd['first_name']). \
            has('lastName', d['last_name']). \
            count(). \
            next()
        count | should.be.equal.to(1)


def test_map_relations(
    graph_client,  # type: GraphClient
    gremlin_url,  # type: str
):
    graph_name = str(uuid4()).replace('-', '')
    graph_client.create_graph(graph_name)
    graph_client.setup_traversal(graph_name)
    gt = GraphTraversal.from_url(
        gremlin_url,
        '{0}_traversal'.format(graph_name)
    )

    mapping = Mapping(
        label='Person',
        name='person',
        keys=[
            KeyMapping(
                name='identifier'
            )
        ],
        properties=[
            PropertyMapping(
                name='identifier',
                source='ID',
            ),
            PropertyMapping(
                name='firstName',
                source='first_name',
                merge_behavior=merge_always,
            ),
            PropertyMapping(
                name='lastName',
                source='last_name',
                merge_behavior=merge_always,
            ),
        ],
        relations=[
            Mapping(
                name='credit_card',
                label='CreditCard',
                keys=[
                    KeyMapping(
                        name='cardNumber',
                    )
                ],
                properties=[
                    PropertyMapping(
                        name='cardNumber',
                        source='card_number',
                    ),
                    PropertyMapping(
                        name='expires',
                        source='expires',
                        merge_behavior=merge_always,
                    ),
                ],
            ).to_dict(),
        ],
    )

    data = [
        {
            'ID': fake.ssn(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'card_number': fake.credit_card_number(),
            'expires': fake.credit_card_expire(),
        } for i in range(1, 10)
    ]

    gt.map_data(mapping=mapping, data=data)

    node_count = gt.g.V().hasLabel(mapping.relations[0].label).count().next()
    node_count | should.be.equal.to(len(data))

    node_count = gt.g.V().hasLabel(mapping.label).count().next()
    node_count | should.be.equal.to(len(data))

    for d in data:
        count = gt.g.V().hasLabel(mapping.label). \
            has('identifier', d['ID']). \
            has('firstName', d['first_name']). \
            has('lastName', d['last_name']). \
            count(). \
            next()
        count | should.be.equal.to(1)

        count = gt.g.V().hasLabel(mapping.relations[0].label). \
            has('cardNumber', d['card_number']). \
            has('expires', d['expires']). \
            count(). \
            next()
        count | should.be.equal.to(1)

        count = gt.g.V().hasLabel(mapping.label). \
            has('identifier', d['ID']). \
            has('firstName', d['first_name']). \
            has('lastName', d['last_name']). \
            outE('credit_card'). \
            as_('e'). \
            inV(). \
            hasLabel(mapping.relations[0].label). \
            has('cardNumber', d['card_number']). \
            has('expires', d['expires']). \
            select('e'). \
            count().next()
        count | should.be.equal.to(1)


def check_mapping(gt: GraphTraversal, mapping: Mapping, data: Iterable[Dict[str, Any]]):
    def _collect_labels(mapping: Mapping) -> Set[str]:
        labels = set([mapping.label])
        if mapping.relations == None:
            return labels
        for rel in mapping.relations:
            labels = labels.union(_collect_labels(rel))
        return labels

    def _matching_nodes(
        gt: GraphTraversal,
        mapping: Mapping,
        data: Iterable[Dict[str, Any]],
        hashes: List[int],
    ) -> Dict[str, Tuple[int, int]]:
        matches_tot: Dict[str, Tuple[int, int]] = {
            mapping.label: (0, 0),
        }
        for row in data:
            keys = frozenset([('label', mapping.label)] +
                             [(p.name, row[p.source]) for p in mapping.key_properties()])
            hashed = hash(keys)
            if hashed in hashes:
                continue
            hashes.append(hashed)
            q = reduce(
                lambda q, k: q.has(k.name, row[k.source]),
                mapping.key_properties(),
                gt.g.V().hasLabel(mapping.label)
            ).count()
            count = q.next()
            (cnt, tot) = matches_tot[mapping.label]
            matches_tot[mapping.label] = (cnt + count, tot + 1)
        if mapping.relations == None:
            return matches_tot
        for rel in mapping.relations:
            submatches = _matching_nodes(gt, rel, data, hashes)
            for k in submatches.keys():
                if k in matches_tot:
                    (cnt, tot) = matches_tot[k]
                    (cnt1, tot1) = submatches[k]
                    matches_tot[k] = (cnt + cnt1, tot + tot1)
                else:
                    matches_tot[k] = submatches[k]
        return matches_tot

    def _apply(
        gt: GraphTraversal,
        mapping: Mapping,
        data: Iterable[Dict[str, Any]],
        nodes_by_label: Dict[str, Dict[int, Dict[str, Any]]],
    ) -> None:
        if mapping.label not in nodes_by_label:
            nodes_by_label[mapping.label] = dict()
            q = gt.g.V().hasLabel(mapping.label).valueMap().by(unfold())
            while q.hasNext():
                values = q.next()
                keys = frozenset([('label', mapping.label)] +
                                 [(p.name, values[p.name]) for p in mapping.key_properties()])
                hashed = hash(keys)
                nodes_by_label[mapping.label][hashed] = values.copy()
        for row in data:
            nodes = nodes_by_label[mapping.label]
            keys = frozenset([('label', mapping.label)] +
                             [(p.name, row[p.source]) for p in mapping.key_properties()])
            hashed = hash(keys)
            if hashed not in nodes:
                nodes[hashed] = {
                    p.name: row[p.source]
                    for p in mapping.properties
                }
            values = nodes[hashed]
            for p in mapping.properties:
                if p.merge_behavior == merge_always:
                    values[p.name] = row[p.source]
                elif p.merge_behavior == merge_if_not_present:
                    if p.name not in values:
                        values[p.name] = row[p.source]
                else:
                    raise Exception(
                        'unsupported merge behavior ' + p.merge_behavior)
        if mapping.relations == None:
            return
        for rel in mapping.relations:
            _apply(gt, rel, data, nodes_by_label)

    labels = _collect_labels(mapping)
    counts_before = {
        label: gt.g.V().hasLabel(label).count().next() for label in labels
    }
    matches_before = _matching_nodes(gt, mapping, data, [])

    gt.map_data(mapping=mapping, data=data)

    counts_after = {
        label: gt.g.V().hasLabel(label).count().next() for label in labels
    }
    matches_after = _matching_nodes(gt, mapping, data, [])

    nodes_by_label: Dict[str, Dict[int, Dict[str, Any]]] = dict()
    _apply(gt, mapping, data, nodes_by_label)

    for label in labels:
        (count, total) = matches_after[label]
        count | should.be.equal.to(total)

        initial = counts_before[label]
        (matches, total) = matches_before[label]

        initial + (total - matches) | should.be.equal.to(counts_after[label])

        nodes = nodes_by_label[label]
        for key in nodes.keys():
            node = nodes[key]
            q = reduce(
                lambda q, pname: q.has(pname, node[pname]),
                node.keys(),
                gt.g.V().hasLabel(label)
            ).count()
            count = q.next()
            count | should.be.equal.to(1)


def test_map_traffico(
    graph_client,  # type: GraphClient
    gremlin_url,  # type: str
):
    graph_name = str(uuid4()).replace('-', '')
    graph_client.create_graph(graph_name)
    graph_client.setup_traversal(graph_name)
    gt = GraphTraversal.from_url(
        gremlin_url,
        '{0}_traversal'.format(graph_name)
    )

    dt = DataLoader()
    data = dt.load(
        'test_data/7154244_traffico_001.csv',
        'Tipo == 1 or Tipo == 2 or Tipo == 6'
    )
    mapping = Mapping(
        label='Persona',
        name='persona',
        keys=[
            KeyMapping(
                name='numeroTelefono'
            ),
        ],
        properties=[
            PropertyMapping(
                name='numeroTelefono',
                source='Chiamante'
            ),
            PropertyMapping(
                name='origine',
                source='Origine / Smcs / Digitato'
            ),
            PropertyMapping(
                name='dataInizio',
                source='Data e Ora Inizio'
            ),
            PropertyMapping(
                name='dataFine',
                source='Data e Ora Fine'
            ),
            PropertyMapping(
                name='tipo',
                source='Tipo'
            ),
            PropertyMapping(
                name='tipo',
                source='Tipo'
            ),
        ],
        relations=[
            Mapping(
                label='Persona',
                name='Telefonato',
                keys=[
                    KeyMapping(
                        name='numeroTelefono'
                    ),
                ],
                properties=[
                    PropertyMapping(
                        name='numeroTelefono',
                        source='Chiamato'
                    )
                ]
            ).to_dict()
        ],
    )
    check_mapping(gt, mapping, data)
    q = gt.g.V().elementMap()
    hashes = []
    while q.hasNext():
        values: Dict[str, Any] = q.next()
        hashes.append(hash(frozenset(values.items())))
    first_hash = hash(frozenset(hashes))

    # check mapping idempotent
    check_mapping(gt, mapping, data)
    q = gt.g.V().elementMap()
    hashes = []
    while q.hasNext():
        values: Dict[str, Any] = q.next()
        hashes.append(hash(frozenset(values.items())))
    recomputed_hash = hash(frozenset(hashes))

    first_hash | should.be.equal.to(recomputed_hash)

    gt.remove_all_vertexes()
