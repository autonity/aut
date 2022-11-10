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

# Create new key.  Use --show-password to allow stdin to be piped to
# the password prompts.
echo -e "\n\n" | aut account new --key-file keystore/dave.key --show-password
(echo -e "\n\n" | aut account new --key-file keystore/dave.key --show-password) && (
    echo "ERROR: account new succeeded with existing file"; exit 1)

# Make a fake transaction and test signing using the new key
aut maketx --key-file keystore/dave.key --to 0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf --value '0.001kwei' --gas 1000 > test.tx
KEYFILEPWD="" aut signtx --key-file keystore/dave.key test.tx > test.signed.tx

popd

set +e
set +x
