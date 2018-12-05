MNEMONIC="text fall reveal replace bonus combine swap goat air bonus submit repair"
GANACHE_PORT=9431
GANACHE_HOST=0.0.0.0
export GANACHE_TARGET=http://$(GANACHE_HOST):$(GANACHE_PORT)
GANACHE=ganache-cli\
			--mnemonic=$(MNEMONIC) \
			--port=$(GANACHE_PORT) \
			--host=$(GANACHE_HOST)

export CONTRACT_BUILD_PATH=$(shell pwd)/src/build

ganache:
	$(GANACHE)

debug:
	$(GANACHE) --verbose --debug

sbt:
	cd scala && sbt

.PHONY: ganache sbt debug
