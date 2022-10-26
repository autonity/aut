.PHONY: tests

setup:
	pip install -e external/autonity.py[dev]
	pip install -e .[dev]

install:
	pipx install . --force

check: check-types check-lint check-format

check-lint:
	pylint autcli tests
	flake8 autcli tests

check-format:
	black --check autcli tests

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
