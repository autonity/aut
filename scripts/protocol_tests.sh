#!/usr/bin/env bash

set -x
set -e

mkdir -p _test_protocol_cli
pushd _test_protocol_cli

../scripts/setup_config_file.sh

echo "aut protocol config"
aut protocol config

echo "aut protocol deployer"
aut protocol deployer

echo "aut protocol epoch-id"
aut protocol epoch-id

echo "aut protocol epoch-reward"
aut protocol epoch-reward

echo "aut protocol epoch-total-bonded-stake"
aut protocol epoch-total-bonded-stake

echo "aut protocol get-bonding-req"
aut protocol get-bonding-req 100 110

echo "aut protocol get-committee"
aut protocol get-committee

echo "aut protocol get-committee-enodes"
aut protocol get-committee-enodes

echo "aut protocol get-last-epoch-block"
aut protocol get-last-epoch-block

echo "aut protocol get-max-committee-size"
aut protocol get-max-committee-size

echo "aut protocol get-minimum-base-fee"
aut protocol get-minimum-base-fee

echo "aut protocol get-operator"
aut protocol get-operator

echo "aut protocol get-proposer"
aut protocol get-proposer 100 3

echo "aut protocol get-unbonding-req"
aut protocol get-unbonding-req 200 220

echo "aut protocol get-validators"
aut protocol get-validators

echo "aut protocol get-version"
aut protocol get-version

echo "aut protocol head-bonding-id"
aut protocol head-bonding-id

echo "aut protocol head-unbonding-id"
aut protocol head-unbonding-id

echo "aut protocol last-epoch-block"
aut protocol last-epoch-block

echo "aut protocol tail-bonding-id"
aut protocol tail-bonding-id

echo "aut protocol tail-unbonding-id"
aut protocol tail-unbonding-id

echo "aut protocol total-redistributed"
aut protocol total-redistributed

set +e
set +x

popd
