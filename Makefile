.PHONY: setup-dev install check check-lint check-format check-types check-tests format tests clean

setup:
	pip install -e ../autonity.py[dev]
	pip install -e .[dev]

install:
	pipx install . --force

check: check-lint check-format check-types

check-lint:
	pylint autcli
	flake8 autcli

check-format:
	black --check autcli

check-types:
	mypy -p autcli -p tests

check-tests tests:
	python -m unittest discover tests

format:
	black autcli/*
	black autcli/commands/*

# tests:
# 	# bash -c "source scripts/run_tests.sh"

clean:
	rm -Rf autcli.egg-info/ build/ .pytest_cache autcli/__pycache__ autcli/commands/__pycache__ tests/__pycache__
