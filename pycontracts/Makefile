HOST_PYTHON ?= python3
PYTEST_ARGS ?=

READLINK :=

# use platform specific readlink
UNAME := $(shell uname)
ifeq ($(UNAME), Linux)
	READLINK := readlink
endif
ifeq ($(UNAME), Darwin)
	READLINK := greadlink
endif

VENV = $(shell $(READLINK) -f ./venv)

export PYTHON = $(VENV)/bin/python3
export PIP = $(VENV)/bin/pip
export PYTEST = $(VENV)/bin/pytest

run: deps
	env -u CONTRACTS_VERSION \
		$(PYTEST) --quiet --disable-warnings $(PYTEST_ARGS)
	env CONTRACTS_VERSION=v1.0-RC1 \
		$(PYTEST) --quiet --disable-warnings $(PYTEST_ARGS)

wait-for-ganache:
	while ! nc -z $(GANACHE_HOST) $(GANACHE_PORT); do \
	  echo 1>&1 "waiting for ganache...";  \
	  sleep 0.1; \
	done

deps: .requirements.flag
test-deps: deps .requirements.test.flag

.requirements.flag: requirements.txt | $(VENV)
	$(PIP) install -r $<
	touch $@

$(VENV):
	$(HOST_PYTHON) -m venv $@

clean:
	rm -rf .*.flag $(VENV) __pycache__

.PHONY: run deps clean
.PHONY: wait-for-ganache
