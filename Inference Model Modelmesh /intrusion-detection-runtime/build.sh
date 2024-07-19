#!/bin/bash
IMAGE_NAME=6666688889/triton-server:0.0.20
docker build -t $IMAGE_NAME .
docker push $IMAGE_NAME