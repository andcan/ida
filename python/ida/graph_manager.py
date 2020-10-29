from concurrent.futures import Future
from typing import Sequence

from gremlin_python.driver.client import Client


class GraphManager:
    def __init__(self, client):
        # type: (Client) -> None
        self._client = client

    def create_graph(self, name):
        # type (str) -> None
        self.submit('''
map = new HashMap<String, Object>();
map.put("storage.backend", "cql");
map.put("storage.hostname", "jce-cassandra");
map.put("storage.cql.read-consistency-level", "ONE");
map.put("storage.cql.write-consistency-level", "ONE");
map.put("index.search.backend", "elasticsearch");
map.put("index.search.hostname", "jce-elastic");
map.put("index.search.elasticsearch.transport-scheme", "http");
map.put("graph.graphname", "{0}");
ConfiguredGraphFactory.createConfiguration(new MapConfiguration(map));'''.format(name)).result()

    def drop_graph(self, name):
        self.submit('ConfiguredGraphFactory.drop("{0}");'.format(name)).result()

    def graph_names(self):
        # type: () -> Sequence[str]
        return self.submit('ConfiguredGraphFactory.getGraphNames()').result()

    def submit(self, message):
        # type: (str) -> Future[Sequence]
        return self._client.submit(message).all()
