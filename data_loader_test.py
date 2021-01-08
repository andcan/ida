import pandas as pd
from .data import PropertyMapping, merge_if_not_present, Mapping, NodeSchema, PropertySchema, Schema
from data_loader import DataLoader
from faker import Faker
from grappa import should

fake = Faker()


def test_gen_mapping(
):
    schema = Schema(
        nodes=[
            NodeSchema(
                label='Person',
                properties=[
                    PropertySchema(
                        name='identifier',
                        kind='String',
                    ),
                    PropertySchema(
                        name='firstName',
                        kind='String'
                    ),
                    PropertySchema(
                        name='lastName',
                        kind='String'
                    ),
                ]
            ),
            NodeSchema(
                label='CreditCard',
                properties=[
                    PropertySchema(
                        name='cardNumber',
                        kind='String',
                    ),
                    PropertySchema(
                        name='expires',
                        kind='String'
                    ),
                ]
            )
        ]
    )
    data = [
        {
            'ID': fake.ssn(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'card_number': fake.credit_card_number(),
            'expires': fake.credit_card_expire(),
            'random_attr': fake.ssn(),
            'example_attr': fake.ssn(),
        } for _ in range(1, 10)
    ]
    df = pd.DataFrame(data)
    dt = DataLoader()
    mappings = dt.generate_mappings(schema, df)

    mappings | should.have.length.of(2)

    pm = next(filter(lambda e: e.name == 'Person', mappings), None)
    expected = Mapping(
        name='Person',
        label='Person',
        keys=[],
        properties=[
            PropertyMapping(
                name='firstName',
                source='first_name',
                merge_behavior=merge_if_not_present,
            ),
            PropertyMapping(
                name='lastName',
                source='last_name',
                merge_behavior=merge_if_not_present,
            ),
        ]
    )
    pm.to_dict() | should.be.equal.to(expected.to_dict())

    cm = next(filter(lambda e: e.name == 'CreditCard', mappings), None)
    cm.to_dict() | should.be.equal.to(
        Mapping(
            name='CreditCard',
            label='CreditCard',
            keys=[],
            properties=[
                PropertyMapping(
                    name='cardNumber',
                    source='card_number',
                    merge_behavior=merge_if_not_present,
                ),
                PropertyMapping(
                    name='expires',
                    source='expires',
                    merge_behavior=merge_if_not_present,
                ),
            ]
        ).to_dict()
    )
