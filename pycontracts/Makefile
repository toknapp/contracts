VENV = $(shell readlink -f ./venv)
HOST_PYTHON ?= python3

export PYTHON = $(VENV)/bin/python3
export PIP = $(VENV)/bin/pip
export PYTEST = $(VENV)/bin/pytest

run: deps
	$(PYTEST) --quiet --workers 4 --disable-warnings $(PYTEST_ARGS)

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
