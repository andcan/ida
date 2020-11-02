from hypothesis import assume

from .graph_client import GraphClient

# Won't work until drop works, raises flaky
# @given(
#     name=from_regex(r'^[a-zA-Z]\w{63}$')
# )
def test_create_graph(graph_client, graph_name):
    # type: (GraphClient,str) -> None
    names = graph_client.graph_names()
    assume(graph_name not in names) # type: ignore
    graph_client.create_graph(graph_name)
    assert graph_name in graph_client.graph_names()
