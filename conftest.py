from uuid import uuid4

import pytest
from typing import Any

from gremlin_python.driver.client import Client
from .graph_client import GraphClient

@pytest.fixture(scope='module') # type: ignore
def gremlin_client(request):
    # type: (Any) -> Client
    url = getattr(request.module, 'url', 'ws://localhost:8182/gremlin')
    traversal_source = getattr(request.module, 'traversal_source', 'ConfigurationManagementGraph')
    client = Client(url, traversal_source)
    request.addfinalizer(lambda: client.close())
    return client


@pytest.fixture(scope='module') # type: ignore
def graph_client(gremlin_client):
    # type: (Client) -> GraphClient
    graph_client = GraphClient(gremlin_client)
    return graph_client


@pytest.fixture(scope='module') # type: ignore
def gremlin_url(request):
    # type: (Any) -> str
    return getattr(request.module, 'url', 'ws://localhost:8182/gremlin')


@pytest.fixture() # type: ignore
def graph_name():
    # type: () -> str
    return unicode('g_' + str(uuid4()).replace('-', ''), 'utf-8') # type: ignore
