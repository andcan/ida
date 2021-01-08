#!/usr/bin/env python

from typing import Optional
import fire
from data_loader import DataLoader
from graph_traversal import GraphTraversal
from graph_client import GraphClient
from gremlin_python.driver.client import Client
import sys
from data import merge_if_not_present, merge_always, NodeSchema, Mapping, PropertyMapping, KeyMapping
import yaml


def init(gremlin_url: str, graph: str, inmemory: bool, create: bool = False) -> GraphTraversal:
    client = Client(gremlin_url, 'ConfigurationManagementGraph')
    graph_client = GraphClient(client, inmemory=inmemory)
    graphs = graph_client.graph_names()
    if not graph in graphs:
        if not create:
            raise Exception('graph {} does not exist.'.format(graph))
        graph_client.create_graph(graph)
    graph_client.setup_traversal(graph)

    return GraphTraversal.from_url(
        gremlin_url,
        '{0}_traversal'.format(graph)
    )


def load_mapping(mapping: str):
    with open(mapping, 'r') as file:
        mapping_content = yaml.load(file.read(), Loader=yaml.FullLoader)
        return Mapping.from_dict(mapping_content)


def check_merge_behavior(merge_behavior):
    if merge_behavior not in [merge_if_not_present, merge_always]:
        raise Exception(
            'invalid merge behavior: {}'.format(merge_behavior)
        )


class CliEditMapping(object):
    def add_property(
        self,
        mapping: str,
        name: str,
        source: str,
        merge_behavior: str = merge_if_not_present,
        kind: Optional[str] = None,
        format: Optional[str] = None
    ):
        check_merge_behavior(merge_behavior)
        m = load_mapping(mapping)
        for p in m.properties:
            if p.name == name:
                raise Exception(
                    'cannot add property <{}>: mapping already exists: {}'.format(name, p))
        m.properties.append(
            PropertyMapping(
                name=name,
                source=source,
                merge_behavior=merge_behavior,
                kind=kind,
                format=format,
            )
        )
        with open(mapping, 'w') as file:
            file.write(m.to_yaml())
        return 'ok'

    def add_key(self, mapping: str, name: str):
        m = load_mapping(mapping)
        for k in m.keys:
            if k.name == name:
                return 'cannot add key <{}>: key already exists: {}'.format(
                    name, k)
        for p in m.properties:
            if p.name == name:
                m.keys.append(
                    KeyMapping(
                        name=name,
                    )
                )
                with open(mapping, 'w') as file:
                    file.write(m.to_yaml())
                return 'ok'
        return 'cannot add key: no such property: <{}>'.format(name)

    def delete_property(self, mapping: str, name: str):
        m = load_mapping(mapping)
        l = len(m.properties)
        m.properties = list(
            filter(
                lambda e: e.name != name,
                m.properties,
            )
        )
        if len(m.properties) != l:
            with open(mapping, 'w') as file:
                file.write(m.to_yaml())
                return 'ok'
        return 'property <{}> not found'.format(name)

    def delete_key(self, mapping: str, name: str):
        m = load_mapping(mapping)
        l = len(m.keys)
        m.keys = list(
            filter(
                lambda e: e.name != name,
                m.keys,
            )
        )
        if len(m.keys) != l:
            with open(mapping, 'w') as file:
                file.write(m.to_yaml())
                return 'ok'
        return 'key <{}> not found'.format(name)


class CliMapping(object):

    def __init__(self, gremlin_url: str, inmemory: bool):
        self.gremlin_url = gremlin_url
        self.inmemory = inmemory

    def apply(
        self,
        input: str,
        mapping: str,
        graph: str,
        create: bool = False,
        query: Optional[str] = None,
        path: Optional[str] = None,
    ) -> str:
        gt = init(
            gremlin_url=self.gremlin_url,
            graph=graph,
            create=create,
            inmemory=self.inmemory
        )
        dt = DataLoader()
        df = dt.load(input, query=query, path=path)
        m = load_mapping(mapping)
        gt.map_data(m, df)
        return 'ok'

    def generate(
        self,
        input: str,
        graph: str,
        label: str,
        create: bool = False,
        map_all: bool = False,
        tolerance: float = 0.5,
        query: Optional[str] = None,
        path: Optional[str] = None,
    ) -> str:
        gt = init(
            gremlin_url=self.gremlin_url,
            graph=graph,
            create=create,
            inmemory=self.inmemory
        )
        dt = DataLoader()
        df = dt.load(input, query=query, path=path)
        schema = gt.schema()
        if label == '*':
            mappings = dt.generate_mappings(
                schema,
                df,
                map_all=map_all,
                tolerance=tolerance,
            )
            str = '---\n'.join([m.to_yaml() for m in mappings])
            return str

        node = None
        for n in schema.nodes:
            if n.label == label:
                node = n
                break
        if node is None:
            node = NodeSchema(
                label=label,
                properties=[]
            )
        mapping = dt.generate_mapping(
            node=node,
            df=df,
            map_all=map_all,
            tolerance=tolerance,
        )
        if mapping is None:
            return ''
        return mapping.to_yaml()


class Cli(object):

    def __init__(self, gremlin_url: str = 'ws://jce-janusgraph:8182/gremlin', inmemory: bool = False):
        self.gremlin_url = gremlin_url
        self.mapping = CliMapping(
            gremlin_url=gremlin_url,
            inmemory=inmemory,
        )
        self.edit_mapping = CliEditMapping()


if __name__ == '__main__':
    # try:
    fire.Fire(Cli)
    # except Exception as e:
    #     print(e, file=sys.stderr)