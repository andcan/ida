from typing import Any, Optional, Sequence

from gremlin_python.driver.client import Client


class GraphClient:
    def __init__(self, client, inmemory=False):
        # type: (Client, Optional[bool]) -> None
        self._client = client
        self._inmemory = inmemory

    def create_graph(self, name):
        # type: (str) -> None
        if self._inmemory:
            self.submit_lines([
                'map = new HashMap<String, Object>();[]',
                'map.put("storage.backend", "inmemory");[]',
                'map.put("graph.graphname", "{0}");[]'.format(name),
                'ConfiguredGraphFactory.createConfiguration(new MapConfiguration(map));[]'
            ])
        else:
            self.submit_lines([
                'map = new HashMap<String, Object>();[]',
                'map.put("storage.backend", "cql");[]',
                'map.put("storage.hostname", "jce-cassandra");[]',
                'map.put("index.search.backend", "elasticsearch");[]',
                'map.put("index.search.hostname", "jce-elastic");[]',
                'map.put("index.search.elasticsearch.transport-scheme", "http");[]',
                'map.put("graph.graphname", "{0}");[]'.format(name),
                'ConfiguredGraphFactory.createConfiguration(new MapConfiguration(map));[]'
            ])

    def drop_graph(self, name):
        # type: (str) -> None
        if isinstance(name, unicode): # type: ignore
            name = str(name)
        self.submit('ConfiguredGraphFactory.drop("{0}");'.format(name))

    def graph_names(self):
        # type: () -> Sequence[str]
        return self.submit('ConfiguredGraphFactory.getGraphNames()')

    def setup_traversal(self, graph_name):
        # type: (str) -> None
        if isinstance(graph_name, unicode): # type: ignore
            graph_name = str(graph_name)
        self.submit('g = ConfiguredGraphFactory.open("{0}").traversal();[]'.format(graph_name))

    def submit_one(self, message):
        # type: (str) -> Any
        return self._client.submit(message).one().result()

    def submit(self, message):
        # type: (str) -> Any
        return self._client.submit(message).all().result()

    def submit_lines(self, lines):
        # type: (Sequence[str]) -> Any
        message = ''  # type: str
        for line in lines:
            message += line
            message += '\n'

        return self.submit(message)

    def load_graph_of_the_gods(self, graph_name, create=False):
        # type: (str, bool) -> None
        if isinstance(graph_name, unicode): # type: ignore
            graph_name = str(graph_name)
        if create:
            self.create_graph(graph_name)
        if self._inmemory:
            message = 'GraphOfTheGodsFactory.loadWithoutMixedIndex(ConfiguredGraphFactory.open("{0}"), true);[]'
        else:
            message = 'GraphOfTheGodsFactory.load(ConfiguredGraphFactory.open("{0}"));[]'
        self.submit(message.format(graph_name))
        self.setup_traversal(graph_name)
