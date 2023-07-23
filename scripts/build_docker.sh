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
if [[ $(docker image ls | grep cochaviz/academic_markdown) ]]; then
    echo "$PREAMBLE Found docker image (cochaviz/academic_markdown), skipping build..."

    if ! [[ $1 = "-f" ]]; then
        exit 0
    fi
fi

docker build -t cochaviz/academic_markdown .devcontainer/