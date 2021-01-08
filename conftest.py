from uuid import uuid4

import pytest
from typing import Any

from gremlin_python.driver.client import Client
from .graph_client import GraphClient

import grappa

grappa.config.show_code = False


@pytest.fixture(scope='module')  # type: ignore
def gremlin_client(request):
    # type: (Any) -> Client
    url = getattr(request.module, 'url', 'ws://jce-janusgraph:8182/gremlin')
    traversal_source = getattr(
        request.module, 'traversal_source', 'ConfigurationManagementGraph')
    client = Client(url, traversal_source)
    request.addfinalizer(lambda: client.close())
    return client


@pytest.fixture(scope='module')  # type: ignore
def graph_client(request, gremlin_client):
    # type: (Any, Client) -> GraphClient
    inmemory = getattr(request.module, 'inmemory', True)
    graph_client = GraphClient(gremlin_client, inmemory=inmemory)
    return graph_client


@pytest.fixture(scope='module')  # type: ignore
def gremlin_url(request):
    # type: (Any) -> str
    return getattr(request.module, 'url', 'ws://jce-janusgraph:8182/gremlin')


@pytest.fixture()  # type: ignore
def graph_name() -> str:
    return 'g_' + str(uuid4()).replace('-', '')
