#!/bin/bash


while [[ "$#" -gt 0 ]]; do
    case $1 in
        -t|--type) TYPE="$2"; shift ;;
        # --nocache) NOCACHE="true" ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Get directory of this script
SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
DOCKER_DIR=${SOURCE_DIR}/docker

IMAGE_NAME=mmdet3d



if [[ ${TYPE} == 'base' ]];then
    IMAGE_NAME=mmdet3d:base
    DOCKER_BUILDKIT=1 docker build --build-arg CACHEBUST=$(date +%s) -f ./docker/Dockerfile.base --no-cache -t ${IMAGE_NAME} ${DOCKER_DIR}
elif [[ ${TASK} == "streampetr" ]];then
    IMAGE_NAME=mmdet3d:streampetr
    DOCKER_BUILDKIT=1 docker build --build-arg CACHEBUST=$(date +%s) -f ./docker/Dockerfile.temporal --no-cache -t ${IMAGE_NAME} ${DOCKER_DIR}
fi