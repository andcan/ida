
from gremlin_python.process.graph_traversal import min_
from hypothesis.strategies._internal.core import lists, sampled_from
from data import NodeSchema, PropertySchema, merge_always, merge_if_not_present
from graph_client import GraphClient
from graph_traversal import GraphTraversal
from datetime import timedelta
from uuid import uuid4
from graph_traversal import GraphTraversal
from hypothesis.strategies._internal.strategies import SearchStrategy
from data import KeyMapping, Mapping, PropertyMapping
from typing import Any, Callable, Dict, Sequence, Tuple
from graph_client import GraphClient
import hypothesis.strategies as st
from hypothesis import given, settings, Verbosity
from typing import Sequence
from grappa import should
from funcy.colls import merge
import string
from faker import Faker

fake = Faker()


def test_node_info(graph_client, gremlin_url, graph_name):
    # type: (GraphClient, str, str) -> None
    graph_name = 'graph_of_the_gods_' + graph_name
    graph_client.load_graph_of_the_gods(graph_name, create=True)
    gt = GraphTraversal.from_url(
        gremlin_url, '{0}_traversal'.format(graph_name))
    schema = gt.schema()
    assert NodeSchema(
        label=u'monster',
        properties=[
            PropertySchema(name=u'name', kind=u'String'),
        ]) in schema.nodes
    assert NodeSchema(
        label=u'god',
        properties=[
            PropertySchema(name=u'age', kind=u'Integer'),
            PropertySchema(name=u'name', kind=u'String'),
        ]) in schema.nodes
    assert NodeSchema(
        label=u'titan',
        properties=[
            PropertySchema(name=u'age', kind=u'Integer'),
            PropertySchema(name=u'name', kind=u'String'),
        ]) in schema.nodes
    assert NodeSchema(
        label=u'demigod',
        properties=[
            PropertySchema(name=u'age', kind=u'Integer'),
            PropertySchema(name=u'name', kind=u'String'),
        ]) in schema.nodes
    assert NodeSchema(
        label=u'human',
        properties=[
            PropertySchema(name=u'age', kind=u'Integer'),
            PropertySchema(name=u'name', kind=u'String'),
        ]) in schema.nodes
    assert NodeSchema(
        label=u'location',
        properties=[
            PropertySchema(name=u'name', kind=u'String'),
        ]) in schema.nodes


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
                relations=[],
            ),
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
