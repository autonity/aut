.PHONY: tests

setup:
	pip --require-virtualenv install -e .[dev]
	pip --require-virtualenv install -e external/autonity.py

check: lint test 

lint:
	hatch run lint

test:
	hatch run test

format:
	hatch run format


# tests:
# 	# bash -c "source scripts/run_tests.sh"

clean:
	hatch clean
