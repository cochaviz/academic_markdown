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

docker build -t cochaviz/academic_markdown .devcontainer/