.PHONY: install lint format tests clean

install:
	pipx install . --force

lint:
	pipenv run pylint autcli

format:
	black autcli/*
	black autcli/commands/*

tests:
	bash -c "source scripts/run_tests.sh"

clean:
	rm -Rf autcli.egg-info/ build/ .pytest_cache autcli/__pycache__ autcli/commands/__pycache__ tests/__pycache__
