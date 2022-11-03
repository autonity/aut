#!/usr/bin/env bash

set -x
set -e

mkdir -p _test_autonity_getters
pushd _test_autonity_getters

../scripts/setup_config_file.sh

echo "aut autonity config"
aut autonity config

echo "aut autonity deployer"
aut autonity deployer

echo "aut autonity epoch-id"
aut autonity epoch-id

echo "aut autonity epoch-reward"
aut autonity epoch-reward

echo "aut autonity epoch-total-bonded-stake"
aut autonity epoch-total-bonded-stake

echo "aut autonity get-bonding-req"
aut autonity get-bonding-req 100 110

echo "aut autonity get-committee"
aut autonity get-committee

echo "aut autonity get-committee-enodes"
aut autonity get-committee-enodes

echo "aut autonity get-last-epoch-block"
aut autonity get-last-epoch-block

echo "aut autonity get-max-committee-size"
aut autonity get-max-committee-size

echo "aut autonity get-minimum-base-fee"
aut autonity get-minimum-base-fee

echo "aut autonity get-operator"
aut autonity get-operator

echo "aut autonity get-proposer"
aut autonity get-proposer 100 3

echo "aut autonity get-unbonding-req"
aut autonity get-unbonding-req 200 220

echo "aut autonity get-validators"
aut autonity get-validators > validators
cat validators
v1=$(head -n1 validators)

echo "aut autonity get-validator"
aut autonity get-validator ${v1}

echo "aut autonity get-version"
aut autonity get-version

echo "aut autonity head-bonding-id"
aut autonity head-bonding-id

echo "aut autonity head-unbonding-id"
aut autonity head-unbonding-id

echo "aut autonity last-epoch-block"
aut autonity last-epoch-block

echo "aut autonity tail-bonding-id"
aut autonity tail-bonding-id

echo "aut autonity tail-unbonding-id"
aut autonity tail-unbonding-id

echo "aut autonity total-redistributed"
aut autonity total-redistributed

popd
