#!/usr/bin/env bash
#
# For more information:
# https://docs.docker.com/engine/reference/commandline/build/
#
# academic_markdown.py will look for a docker image with the name
# cochaviz/academic_markdown which is why this was provided 
# specifically. At some point I will probably add it to a container
# registry and you won't need to run this anymore.
#

PREAMBLE="academic_markdown (build_docker.sh):"

# if container is installed, its fine
if [[ $(docker image ls | grep zoharcochavi/academic-markdown) ]]; then
    # unless someone really wants to build
    if [[ ! $# || ! $1 = "-f" ]]; then
        echo "$PREAMBLE Found docker image (zoharcochavi/academic-markdown), skipping build..."
        exit 0
    fi
    # remove -f option (the rest are build commands)
    shift
fi

# if there are no build commands
if [[ $# ]]; then
    echo "$PREAMBLE Attempting to pull from registry"
    docker pull zoharcochavi/academic-markdown 
fi

# if there are explit build commands or the previous failed
if [[ $?  || ! $# ]]; then
    echo "$PREAMBLE Pulling unuccessful, or explicit build arguments given, building locally"
    docker build -t zoharcochavi/academic-markdown $@ .devcontainer/
fi

exit $?