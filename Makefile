MNEMONIC="text fall reveal replace bonus combine swap goat air bonus submit repair"
GANACHE_PORT ?= 9431
GANACHE_HOST ?= 127.0.0.1
export GANACHE_TARGET=http://$(GANACHE_HOST):$(GANACHE_PORT)
GANACHE=ganache-cli\
			--mnemonic=$(MNEMONIC) \
			--port=$(GANACHE_PORT) \
			--host=$(GANACHE_HOST)

DOCKER ?= docker
DOCKER_IMAGE ?= contracts

export CONTRACT_BUILD_PATH ?= $(shell pwd)/src/build

ganache:
	$(GANACHE)

debug:
	$(GANACHE) --verbose --debug

contracts:
	$(MAKE) -C src

test: contracts
	$(MAKE) -C pycontracts run

repl: contracts
	PYTHONPATH=.:$(PYTHONPATH) python -i pycontracts/tests/test_settings.py

docker-image:
	$(DOCKER) build -t $(DOCKER_IMAGE) .

run-docker: docker-image
	$(DOCKER) run \
		--net=host \
		-e GANACHE_TARGET=$(GANACHE_TARGET) \
		$(DOCKER_IMAGE) run

clean:
	$(MAKE) -C src clean
	$(MAKE) -C pycontracts clean

.PHONY: ganache
.PHONY: debug test repl contracts
.PHONY: clean
