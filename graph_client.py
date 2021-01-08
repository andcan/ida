from typing import Any, Sequence

from gremlin_python.driver.client import Client


class GraphClient:
    def __init__(self, client: Client, inmemory: bool = False):
        self._client = client
        self._inmemory = inmemory

    def create_graph(self, name: str) -> None:
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

    def drop_graph(self, name: str) -> None:
        if isinstance(name, unicode):  # type: ignore
            name = str(name)
        self.submit('ConfiguredGraphFactory.drop("{0}");'.format(name))

    def graph_names(self) -> Sequence[str]:
        return self.submit('ConfiguredGraphFactory.getGraphNames()')

    def setup_traversal(self, graph_name: str) -> None:
        self.submit(
            'g = ConfiguredGraphFactory.open("{0}").traversal();[]'.format(graph_name))

    def submit_one(self, message: str) -> Any:
        return self._client.submit(message).one().result()

    def submit(self, message: str) -> Any:
        return self._client.submit(message).all().result()

    def submit_lines(self, lines: Sequence[str]) -> Any:
        message = ''
        for line in lines:
            message += line
            message += '\n'

        return self.submit(message)

    def load_graph_of_the_gods(self, graph_name: str, create: bool = False) -> None:
        if create:
            self.create_graph(graph_name)
        if self._inmemory:
            message = 'GraphOfTheGodsFactory.loadWithoutMixedIndex(ConfiguredGraphFactory.open("{0}"), true);[]'
        else:
            message = 'GraphOfTheGodsFactory.load(ConfiguredGraphFactory.open("{0}"));[]'
        self.submit(message.format(graph_name))
        self.setup_traversal(graph_name)
