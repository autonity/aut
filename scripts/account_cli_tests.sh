#!/usr/bin/env bash

set -x
set -e

mkdir -p _test_accounts_cli
pushd _test_accounts_cli

../scripts/setup_config_file.sh

aut account list
aut account info
aut account info --key-file keystore/bob.key
aut account balance

popd

set +e
set +x
