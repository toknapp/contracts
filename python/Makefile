VENV = $(shell readlink -f ./venv)
HOST_PYTHON ?= python3

export PYTHON = $(VENV)/bin/python3
export PIP = $(VENV)/bin/pip
export PYTEST = $(VENV)/bin/pytest

run: deps
	$(PYTEST) -v --disable-warnings

repl:
	$(PYTHON) -i test_settings.py

deps: .requirements.flag
test-deps: deps .requirements.test.flag

.requirements.flag: requirements.txt | $(VENV)
	$(PIP) install -r $<
	touch $@

$(VENV):
	$(HOST_PYTHON) -m venv $@

clean:
	rm -rf .*.flag $(VENV)

.PHONY: run deps clean
