#!/usr/bin/env bash

DOCKER_IMAGE="zoharcochavi/academic-markdown"
PREAMBLE="academic_markdown (check_health.sh):"
GOOD="✅"
BAD="⚠️"

HEALTH=0

check_in_path() {
    if [[ $(type -P "$1") ]]; then
        echo "$PREAMBLE $GOOD Found ($1) in path"
        return 0
    else
        echo "$PREAMBLE $BAD Could not find ($1) in path"
        return 1
    fi
}

check_docker() {
    check_in_path "docker" 

    if ! [[ $? ]]; then
        echo "$PREAMBLE ℹ️ Running docker health check..."

        docker run hello-world
        if ! [[ $? ]]; then
            echo "$PREAMBLE $GOOD Docker correctly configured"
        else
            echo "$PREAMBLE $BAD Docker does not seem to be configured correctly"
            return 1
        fi

        if ! [[ $(docker images | grep $DOCKER_IMAGE) ]]; then
            echo "$PREAMBLE $GOOD Found '$DOCKER_IMAGE' docker image"
        else
            echo "$PREAMBLE ℹ️ Could not find image '$DOCKER_IMAGE'."
            echo "$PREAMBLE ℹ️ Running build_docker script to resolve..."

            if [[ $(./scripts/build_docker.sh) ]]; then
                echo "$PREAMBLE $GOOD Fixed Docker setup!"
            else
                echo "$PREAMBLE $BAD Could not fix Docker setup automatically, please check the logs to locate the issue."
                return 1
            fi
        fi
    else
        echo "$PREAMBLE ℹ️ Not running docker health check since it cannot be found on path..."
        return 1
    fi

    return 0
}

dependencies=(
    pandoc  
    pandoc-crossref 
    python3
    pdflatex
)

dependencies_optional=(
    tectonic
)

if [[ $1 = "--docker" ]]; then
    check_docker
else
    for dependency in "${dependencies[@]}"; do
        check_in_path $dependency

        if ! [[ $? ]]; then
            HEALTH=1
        fi
    done

    echo "$PREAMBLE ℹ️ The following are optional dependencies."

    for dependency in "${dependencies_optional[@]}"; do
        check_in_path $dependency
    done
fi

if ! [[ HEALTH ]]; then
    exit 1
fi
