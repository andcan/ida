# Setup
## Prerequisites
* [Docker](https://docs.docker.com/get-docker/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Steps
* Adjust `docker-compose.yaml` to your machine specs.   
  `services.{janusgraph|cassandra|elasticsearch}.deploy.resources.limits` contains limits for each container.  
  Notes: `cpus: 1` is one core (0.5 is half core, floats allowed) and memory can be expressed like `1G` or `1024M`.  
  Special attention for cassandra: `HEAP_NEWSIZE` and `MAX_HEAP_SIZE` must be adjusted and are equivalent to JAVA_OPTS `-Xms` `-Xmx`. Java heap should be half of available memory for container (limit: 1G -> MAX_HEAP_SIZE: 512M)
* Start docker daemon  
  Linux:
  ```shell script
  systemctl start docker
  ```
* Execute docker compose(it will take a while):
  ```shell script
  docker-compose up -d # -d makes docker-compose execute in background
  ```
  Use `docker ps` and `docker logs <container_name>` to inspect containers status.  
  It may be necessary to start `jce-janus` container manually (or re-run `docker-compose up`) because of cassandra's slow start.
* Start gremlin console:
  ```shell script
  ./start_gremlin_console.sh
  ```

## Getting feet wet
* Check graph creation works:
  ```groovy
  :remote connect tinkerpop.server conf/remote.yaml session
  :remote console
  map = new HashMap<String, Object>();
  map.put("storage.backend", "cql");
  map.put("storage.hostname", "jce-cassandra");
  map.put("index.search.backend", "elasticsearch");
  map.put("index.search.hostname", "jce-elastic");
  map.put("index.search.elasticsearch.transport-scheme", "http");
  map.put("graph.graphname", "graph1");
  ConfiguredGraphFactory.createConfiguration(new MapConfiguration(map));
  ```
  Then disconnect and reconnect to check if graph exists.
  ```groovy
  :remote connect tinkerpop.server conf/remote.yaml session
  :remote console
  ConfiguredGraphFactory.getGraphNames()
  ```
* Seed database:
  ```groovy
  graph = ConfiguredGraphFactory.open("graph1")
  GraphOfTheGodsFactory.load(graph)
  g = graph.traversal()
  ```
* Follow [this](https://docs.janusgraph.org/getting-started/basic-usage) guide from chapter `Global Graph Indices`

