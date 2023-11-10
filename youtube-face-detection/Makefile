# Copyright (c) Datalayer, Inc. https://datalayer.io
# Distributed under the terms of the MIT License.

.PHONY: clean build push start connect stop rm

help: ## display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

default: all ## default target is all.

all: clean install build ## make clean install build.

clean: ## clean.

build: ## build the image.
	docker build \
		-t ${DATALAYER_DOCKER_REPO}/jupyter-kernel-youtube:0.0.6 \
		.

push: ## push the image.
	docker push \
	    ${DATALAYER_DOCKER_REPO}/jupyter-kernel-youtube:0.0.6

start: ## start the container.
	docker run -it \
		--name datalayer-jupyter-kernel-youtube \
		--rm \
		-p 2522:2522 \
		${DATALAYER_DOCKER_REPO}/jupyter-kernel-youtube:0.0.6

logs: ## show container logs.
	docker logs datalayer-jupyter-kernel-youtube -f

connect: ## connect to the container.
	docker exec -it datalayer-jupyter-kernel-youtube bash

stop: ## stop the container.
	docker stop datalayer-jupyter-kernel-youtube

rm: ## remove the container.
	docker rm -f datalayer-jupyter-kernel-youtube
