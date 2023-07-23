#!/usr/bin/env bash

PREAMBLE="academic_markdown (check_health.sh):"
HEALTH=0

check_in_path() {
    if [[ $(type -P "$1") ]]; then
        echo "$PREAMBLE ✅ Found ($1) in path"
        return 0
    else
        echo "$PREAMBLE ⚠️ Could not find ($1) in path"
        return 1
    fi
}

check_docker() {
    check_in_path "docker"
    if [[ $? ]]; then
        echo "$PREAMBLE ℹ️ Running docker health check..."

        docker run hello-world
        if [[ $? ]]; then
            echo "$PREAMBLE ✅ Docker correctly configured"
        else
            echo "$PREAMBLE ⚠️ Docker does not seem to be configured correctly"
            HEALTH=1
        fi

        if [[ $(docker images | grep cochaviz/academic_markdown) ]]; then
            echo "$PREAMBLE ✅ Found 'cochaviz/academic_markdown' docker image"
        else
            echo "$PREAMBLE ⚠️ Could not find image 'cochaviz/academic_markdown'.\nPlease run the install script (scripts/build_docker.sh) or the corresponding VSCode Task."
            HEALTH=1
        fi
    else
        echo "$PREAMBLE ℹ️ Not running docker health check since it cannot be found on path..."
        HEALTH=1
    fi
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
