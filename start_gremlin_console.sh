#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

docker-compose -f .devcontainer/docker-compose.yaml run --rm \
  -e GREMLIN_REMOTE_HOSTS=janusgraph \
  -v "$DIR"/assets/init.groovy:/opt/janusgraph/init.groovy \
  janusgraph ./bin/gremlin.sh -i init.groovy
