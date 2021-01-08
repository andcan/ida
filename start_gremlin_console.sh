#!/usr/bin/env bash

init_script=$(cat <<EOF
:remote connect tinkerpop.server conf/remote.yaml session
:remote console
EOF
)

docker run --rm -it \
  -e GREMLIN_REMOTE_HOSTS=jce-janusgraph \
  --network ida_devcontainer_jce-network \
  janusgraph/janusgraph bash -c "echo -e '$init_script' > init.groovy && ./bin/gremlin.sh -i init.groovy"