
from .data import NodeSchema, PropertySchema
from .graph_client import GraphClient
from .graph_traversal import GraphTraversal
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection


class TestGraphTraversal:

    def test_node_info(self, graph_client, gremlin_url):
        # type: (GraphClient, str) -> None
        graph_name = 'graph_of_the_gods'
        graph_names = graph_client.graph_names()
        if graph_name not in graph_names:
            graph_client.load_graph_of_the_gods(graph_name, True)

        g = traversal().withRemote(DriverRemoteConnection(
            gremlin_url, '{0}_traversal'.format(graph_name)))
        gt = GraphTraversal(g)
        nodes_schema = gt.nodes_schema()
        assert NodeSchema(
            label=u'monster',
            properties=[
                PropertySchema(name=u'name', kind=u'String'),
            ]) in nodes_schema
        assert NodeSchema(
            label=u'god',
            properties=[
                PropertySchema(name=u'age', kind=u'Integer'),
                PropertySchema(name=u'name', kind=u'String'),
            ]) in nodes_schema
        assert NodeSchema(
            label=u'titan',
            properties=[
                PropertySchema(name=u'age', kind=u'Integer'),
                PropertySchema(name=u'name', kind=u'String'),
            ]) in nodes_schema
        assert NodeSchema(
            label=u'demigod',
            properties=[
                PropertySchema(name=u'age', kind=u'Integer'),
                PropertySchema(name=u'name', kind=u'String'),
            ]) in nodes_schema
        assert NodeSchema(
            label=u'human',
            properties=[
                PropertySchema(name=u'age', kind=u'Integer'),
                PropertySchema(name=u'name', kind=u'String'),
            ]) in nodes_schema
        assert NodeSchema(
            label=u'location',
            properties=[
                PropertySchema(name=u'name', kind=u'String'),
            ]) in nodes_schema
