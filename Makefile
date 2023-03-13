.PHONY: tests

setup:
	pip --require-virtualenv install -e .[dev]
	pip --require-virtualenv install -e external/autonity.py

check: check-types check-lint check-format check-tests

check-lint:
	pylint --ignore-patterns='.*flycheck.*' aut tests
	flake8 aut tests

check-format:
	black --check aut tests

check-types:
	mypy -p aut -p tests

check-tests tests:
	python -m unittest discover tests

format:
	black aut/*
	black aut/commands/*

# tests:
# 	# bash -c "source scripts/run_tests.sh"

clean:
	rm -Rf aut.egg-info/ build/ .pytest_cache aut/__pycache__ aut/commands/__pycache__ tests/__pycache__
