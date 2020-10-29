from unicodedata import category

import pytest
from hypothesis import given, assume
from hypothesis.strategies import text, characters, from_regex
from typing import Any

from gremlin_python.driver.client import Client
from ida.graph_manager import GraphManager


@pytest.fixture(scope='module')
def gremlin_client(request):
    # type: (Any) -> Client
    url = getattr(request.module, 'url', 'ws://localhost:8182/gremlin')
    traversal_source = getattr(request.module, 'traversal_source', 'ConfigurationManagementGraph')
    client = Client(url, traversal_source)
    request.addfinalizer(lambda: client.close())
    return client


@pytest.fixture(scope='module')
def graph_manager(gremlin_client):
    # type: (Client) -> GraphManager
    graph_manager = GraphManager(gremlin_client)
    names = graph_manager.graph_names()
    for graph in names:
        graph_manager.drop_graph(graph)
    return graph_manager


@given(
    name=from_regex(r'[a-zA-Z]\w{63}')
)
def test_create_graph(name, graph_manager):
    # type: (str, GraphManager) -> None
    assume(name not in graph_manager.graph_names())
    graph_manager.create_graph(name)
    assert name in graph_manager.graph_names()
