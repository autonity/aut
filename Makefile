.PHONY: test check lint format clean

check: lint test 

lint:
	hatch run lint

test:
	rm -rf test_*
	hatch run ./scripts/test_contract
	hatch run ./scripts/test_protocol
	hatch run ./scripts/test_validator
	hatch run ./scripts/test_account
	hatch run ./scripts/test_token

format:
	hatch run format


clean:
	hatch clean

# refresh-env is used in development mode when the 
# local dependecy to autonity.py has changed, this is because 
# hatch does not support editable depenedencies
# see https://github.com/pypa/hatch/issues/588
refresh-env:
	hatch env prune
	hatch run true
