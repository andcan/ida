from .graph_client import GraphClient

# @given( # type: ignore
#     name=from_regex(r'^[a-zA-Z]\w{63}$')
# )
def test_create_graph(graph_client, graph_name):
    # type: (GraphClient, str) -> None
    # assume(graph_name not in graph_client.graph_names()) # type: ignore
    graph_client.create_graph(graph_name)
    assert graph_name in graph_client.graph_names()