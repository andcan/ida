#!/usr/bin/env ash

# docker-compose -f .devcontainer/docker-compose.yaml run --rm \
#   -e GREMLIN_REMOTE_HOSTS=jce-janusgraph \
#   -v .devcontainer/janus/init.groovy:/opt/janusgraph/init.groovy \
#   janusgraph ./bin/gremlin.sh -i init.groovy

graph_name="$(tr -dc 'a-f0-9' < /dev/urandom | head -c20)"

init_script=$(cat <<EOF
:remote connect tinkerpop.server conf/remote.yaml session
:remote console
map = new HashMap<String, Object>()
map.put("storage.backend", "inmemory")
map.put("graph.graphname", "$graph_name");
ConfiguredGraphFactory.createConfiguration(new MapConfiguration(map))
graph = ConfiguredGraphFactory.open("$graph_name")
g = graph.traversal()
EOF
)

docker run --rm -it \
  -e GREMLIN_REMOTE_HOSTS=jce-janusgraph \
  --network ida_devcontainer_jce-network \
  janusgraph/janusgraph bash -c "echo -e '$init_script' > init.groovy && ./bin/gremlin.sh -i init.groovy"