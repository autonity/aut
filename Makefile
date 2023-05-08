.PHONY: test check lint format clean

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
