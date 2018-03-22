#
# Copyright (c) 2015 - Present.  Boling Consulting Solutions, BCSW.net
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
ifneq ($(SDNDBG_BUILD),docker)
ifeq ($(SDNDBG_BASE)_set,_set)
$(error To get started, please source the env.sh file)
endif
endif

ifeq ($(TAG),)
TAG := latest
endif

ifeq ($(TARGET_TAG),)
TARGET_TAG := latest
endif

# If no DOCKER_HOST_IP is specified grab a v4 IP address associated with
# the default gateway
ifeq ($(DOCKER_HOST_IP),)
DOCKER_HOST_IP := $(shell ifconfig $$(netstat -rn | grep -E '^(default|0.0.0.0)' | head -1 | awk '{print $$NF}') | grep inet | awk '{print $$2}' | sed -e 's/addr://g')
endif

include setup.mk

ifneq ($(http_proxy)$(https_proxy),)
# Include proxies from the environment
DOCKER_PROXY_ARGS = \
       --build-arg http_proxy=$(http_proxy) \
       --build-arg https_proxy=$(https_proxy) \
       --build-arg ftp_proxy=$(ftp_proxy) \
       --build-arg no_proxy=$(no_proxy) \
       --build-arg HTTP_PROXY=$(HTTP_PROXY) \
       --build-arg HTTPS_PROXY=$(HTTPS_PROXY) \
       --build-arg FTP_PROXY=$(FTP_PROXY) \
       --build-arg NO_PROXY=$(NO_PROXY)
endif

DOCKER_BUILD_ARGS = \
	--build-arg TAG=$(TAG) \
	--build-arg REGISTRY=$(REGISTRY) \
	--build-arg REPOSITORY=$(REPOSITORY) \
	$(DOCKER_PROXY_ARGS) $(DOCKER_CACHE_ARG) \
	 --rm --force-rm \
	$(DOCKER_BUILD_EXTRA_ARGS)

VENVDIR := venv-$(shell uname -s | tr '[:upper:]' '[:lower:]')

DOCKER_IMAGE_LIST = \
    base \
	ubuntu_16_04

# The following list was scavanged from the compose / stack files as well as
# from the Dockerfiles. If nothing else it highlights that SDNdbg is not
# using consistent versions for some of the containers.

# grep  -i "^FROM" docker/Dockerfile.* | grep -v sdndbg-  | sed -e 's/ as .*$//g' -e 's/\${REGISTRY}//g' | awk '{print $NF}' | grep -v '^scratch' | sed '/:.*$/!s/$/:latest/g' | sort -u | sed -e 's/^/       /g' -e 's/$/ \\/g'

FETCH_BUILD_IMAGE_LIST = \
       centos:7 \
       debian:stretch-slim \
       ubuntu:xenial \
       onosproject/onos:1.10.9

## find compose -type f | xargs grep image: | awk '{print $NF}' | grep -v sdndbg- | sed -e 's/\"//g' -e 's/\${REGISTRY}//g' -e 's/:\${.*:-/:/g' -e 's/\}//g' -e '/:.*$/!s/$/:latest/g' | sort -u | sed -e 's/^/        /g' -e 's/$/ \\/g'
FETCH_COMPOSE_IMAGE_LIST = \
        wurstmeister/kafka:latest \
        wurstmeister/zookeeper:latest
#        consul:0.9.2 \
#        docker.elastic.co/elasticsearch/elasticsearch:5.6.0 \
#        fluent/fluentd:latest \
#        fluent/fluentd:v0.12.42 \
#        gliderlabs/registrator:latest \
#        kamon/grafana_graphite:latest \
#        marcelmaatkamp/freeradius:latest \
#        postgres:9.6.1 \
#        quay.io/coreos/etcd:v3.2.9 \
#        registry:2 \
#        tianon/true:latest \

FETCH_IMAGE_LIST = $(shell echo $(FETCH_BUILD_IMAGE_LIST) $(FETCH_COMPOSE_IMAGE_LIST)  | tr ' ' '\n' | sort -u)
NETWORKS = compose_kolla_control compose_kolla_external

.PHONY: $(DIRS) $(DIRS_CLEAN) base kolla-ansible start stop tag push pull networks $(NETWORKS)

.PHONY: start stop

# This should to be the first and default target in this Makefile
help:
	@echo "Usage: make [<target>]"
	@echo "where available targets are:"
	@echo
	@echo "build         : Build the SDNdbg images.\n\
               If this is the first time you are building, choose \"make build\" option."
	@echo "production    : Build SDNdbg for production deployment"
	@echo "clean         : Remove files created by the build and tests"
	@echo "distclean     : Remove venv directory"
	@echo "fetch         : Pre-fetch artifacts for subsequent local builds"
	@echo "help          : Print this help"
	@echo "rebuild-venv  : Rebuild local Python virtualenv from scratch"
	@echo "venv          : Build local Python virtualenv if did not exist yet"
	@echo "containers    : Build all the docker containers"
	@echo "networks"     : Create user-defined networks for development"
	@echo "base          : Build the base docker container used by all other dockers"
	@echo "kolla-ansible : Build the kolla-ansible docker container"
	@echo "utest         : Run all unit tests"
	@echo "itest         : Run all integration tests"
	@echo "test          : Run all unit and integration tests"
	@echo "start         : Start SDNDbg on the current system"
	@echo "stop          : Stop SDNDbg on the current system"
	@echo "tag           : Tag a set of images"
	@echo "push          : Push the docker images to an external repository"
	@echo "pull          : Pull the docker images from a repository"
	@echo
## New directories can be added here
DIRS:=

# Parallel Build
$(DIRS):
	@echo "    MK $@"
	$(Q)$(MAKE) -C $@

# Parallel Clean
DIRS_CLEAN = $(addsuffix .clean,$(DIRS))
$(DIRS_CLEAN):
	@echo "    CLEAN $(basename $@)"
	$(Q)$(MAKE) -C $(basename $@) clean

build: containers networks

production: prod-containers

containers: base kolla-ansible

#containers: base kolla-ansible kolla-ansible-dev

base: docker/Dockerfile.base
	docker build $(DOCKER_BUILD_ARGS) -t ${REGISTRY}${REPOSITORY}sdndbg-base:${TAG} -f docker/Dockerfile.base .

kolla-ansible: docker/Dockerfile.kolla-ansible
	docker build $(DOCKER_BUILD_ARGS) -t ${REGISTRY}${REPOSITORY}sdndbg-kolla-ansible:${TAG} -f docker/Dockerfile.kolla-ansible .

kolla-ansible-dev: docker/Dockerfile.kolla-ansible-dev
	docker build $(DOCKER_BUILD_ARGS) -t ${REGISTRY}${REPOSITORY}sdndbg-kolla-ansible-dev:${TAG} -f docker/Dockerfile.kolla-ansible-dev .

kolla-registry: docker/Dockerfile.registry
	docker build $(DOCKER_BUILD_ARGS) -t ${REGISTRY}${REPOSITORY}sdndbg-kolla-registry:${TAG} -f docker/Dockerfile.registry .

networks: $(NETWORKS)

compose_kolla_control:
	- docker network create --internal compose_kolla_control

compose_kolla_external:
	- docker network create compose_kolla_external

test-containers:
	@ echo 'NEED TO IMPLEMENT'

prod-containers: base kolla-ansible

@MAKE_ENV := $(shell echo '$(.VARIABLES)' | awk -v RS=' ' '/^[a-zA-Z0-9]+$$/')
@SHELL_EXPORT := $(foreach v,$(MAKE_ENV),$(v)='$($(v))')
start:
	$(SHELL_EXPORT) STACK_TEMPLATE=./compose/sdndbg-stack.yml.j2 ./scripts/run-sdndbg.sh start

stop:
	./scripts/run-sdndbg.sh stop

tag: $(patsubst  %,%.tag,$(DOCKER_IMAGE_LIST))

push: tag $(patsubst  %,%.push,$(DOCKER_IMAGE_LIST))

pull: $(patsubst  %,%.pull,$(DOCKER_IMAGE_LIST))

%.tag:
	docker tag ${REGISTRY}${REPOSITORY}sdndbg-$(subst .tag,,$@):${TAG} ${TARGET_REGISTRY}${TARGET_REPOSITORY}sdndbg-$(subst .tag,,$@):${TARGET_TAG}

%.push:
	docker push ${TARGET_REGISTRY}${TARGET_REPOSITORY}sdndbg-$(subst .push,,$@):${TARGET_TAG}

%.pull:
	docker pull ${REGISTRY}${REPOSITORY}sdndbg-$(subst .pull,,$@):${TAG}


clean:
	find . -name '*.pyc' | xargs rm -f

distclean: clean
	rm -rf ${VENVDIR}

fetch:
	@bash -c ' \
		for i in $(FETCH_IMAGE_LIST); do \
			docker pull $$i; \
		done'

purge-venv:
	rm -fr ${VENVDIR}

rebuild-venv: purge-venv venv

ifneq ($(SDNDBG_BUILD),docker)
venv: ${VENVDIR}/.built
else
venv:
endif

${VENVDIR}/.built:
	@ virtualenv ${VENVDIR}
	@ . ${VENVDIR}/bin/activate && \
	    pip install --upgrade pip; \
	    if ! pip install -r requirements.txt; \
	    then \
	        echo "On MAC OS X, if the installation failed with an error \n'<openssl/opensslv.h>': file not found,"; \
	        echo "see the BUILD.md file for a workaround"; \
	    else \
	        uname -s > ${VENVDIR}/.built; \
	    fi

ifneq ($(SDNDBG_BUILD),docker)
test: venv
	@ echo "Executing all tests"
	. ${VENVDIR}/bin/activate && \
	nosetests -s tests
else
test: test_runner
	docker run \
		-e SDNDBG_BUILD=docker \
		-e REGISTRY=${REGISTRY} \
		-e REPOSITORY=${REPOSITORY} \
		-e TAG=${TAG} \
		-e DOCKER_HOST_IP=${DOCKER_HOST_IP} \
		--rm --net=host -v /var/run/docker.sock:/var/run/docker.sock \
		${REGISTRY}${REPSOITORY}sdndbg-test_runner:${TAG} \
		nosetests -s tests
endif

ifneq ($(SDNDBG_BUILD),docker)
utest: venv
	@ echo "Executing all unit tests"
	. ${VENVDIR}/bin/activate && \
	    for d in $$(find ./tests/utests -type d|sort -nr); do echo $$d:; nosetests $$d; done
else
utest: test_runner
	docker run \
		-e SDNDBG_BUILD=docker \
		-e REGISTRY=${REGISTRY} \
		-e REPOSITORY=${REPOSITORY} \
		-e TAG=${TAG} \
		-e DOCKER_HOST_IP=${DOCKER_HOST_IP} \
		--rm --net=host -v /var/run/docker.sock:/var/run/docker.sock \
		${REGISTRY}${REPSOITORY}sdndbg-test_runner:${TAG} \
		bash -c \
		'for d in $$(find ./tests/utests -type d|sort -nr); do \
			echo $$d:; \
			nosetests $$d; \
		done'
endif

ifneq ($(SDNDBG_BUILD),docker)
utest-with-coverage: venv
	@ echo "Executing all unit tests and producing coverage results"
	. ${VENVDIR}/bin/activate && \
        for d in $$(find ./tests/utests -type d|sort -nr); do echo $$d:; \
	nosetests --with-xcoverage --with-xunit --cover-package=sdndbg $$d; done
else
utest-with-coverage: test_runner
	@echo "Executing all unit tests and producing coverage results"
	docker run \
		-e SDNDBG_BUILD=docker \
		-e REGISTRY=${REGISTRY} \
		-e REPOSITORY=${REPOSITORY} \
		-e TAG=${TAG} \
		-e DOCKER_HOST_IP=${DOCKER_HOST_IP} \
		--rm --net=host -v /var/run/docker.sock:/var/run/docker.sock \
		${REGISTRY}${REPSOITORY}sdndbg-test_runner:${TAG} \
		bash -c \
		'for d in $$(find ./tests/utests -type d|sort -nr); do \
			echo $$d:; \
			nosetests --with-xcoverage --with-xunit --cover-package=sdndbg $$d; \
		done'
endif

ifneq ($(SDNDBG_BUILD),docker)
itest: venv
	@ echo "Executing all integration tests"
	. ${VENVDIR}/bin/activate && \
	REGISTRY=${REGISTRY} \
	REPOSITORY=${REPOSITORY} \
	TAG=${TAG} \
	DOCKER_HOST_IP=${DOCKER_HOST_IP} \
	nosetests -s  \
		tests/itests/docutests/build_md_test.py \
		--exclude-dir=./tests/utests/
else
itest: test_runner
	@ echo "Executing all integration tests"
	docker run \
		-e SDNDBG_BUILD=docker \
		-e REGISTRY=${REGISTRY} \
		-e REPOSITORY=${REPOSITORY} \
		-e TAG=${TAG} \
		-e DOCKER_HOST_IP=${DOCKER_HOST_IP} \
		--rm --net=host -v /var/run/docker.sock:/var/run/docker.sock \
		${REGISTRY}${REPSOITORY}sdndbg-test_runner:${TAG} \
		nosetests -s  \
			tests/itests/docutests/build_md_test.py \
			--exclude-dir=./tests/utests/
endif

# end file

