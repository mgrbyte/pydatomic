#
# Make for pydatomic
#
PY3_VERSION ?= $(shell python3 -c 'import sys;print(sys.version_info.major)')
PY2_VERSION ?= $(shell python2 -c 'import sys;print(sys.version_info.major)')
VENV := env-${PY2_VERSION}
VENV3 := env-${PY3_VERSION}

.PHONY: all
all:

.PHONY: test
test: test-unit test-flake8

.PHONY: test-unit
test-unit:
	@${VENV}/bin/py.test tests
	@${VENV3}/bin/py.test tests

.PHONY: test-flake8
test-flake8:
	@${VENV}/bin/flake8 --config=tests/flake8.rc pydatomic
	@${VENV3}/bin/flake8 --config=tests/flake8.rc pydatomic

.PHONY: coverage
coverage:
# TDB:
	@${VENV}/bin/py.test --cov=pydatomic tests

.PHONY: prepare-venv
prepare-venv:
	@virtualenv -p python${PY2_VERSION} ${VENV}
	@${VENV}/bin/pip install --upgrade -r requirements.txt
	@virtualenv -p python${PY3_VERSION} ${VENV3}
	@${VENV3}/bin/pip install --upgrade -r requirements.txt
