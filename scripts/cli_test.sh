#!/usr/bin/env bash

set -x
set -e

# Test assumes a live testnet, and relies on Alice having some funds.
# Got to: https://faucet.autonity.org/ to recharge.
export WEB3_ENDPOINT="https://rpc1.piccadilly.autonity.org:8545/"

# We use these dummy Dummy keys:
ALICE=0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf
ALICE_KEYFILE=../tests/data/alice.key

BOB=0x2B5AD5c4795c026514f8317c7a215E218DcCD6cF
BOB_KEYFILE=../tests/data/bob.key

CAROL=0x6813Eb9362372EEF6200f3b1dbC3f819671cBA69

mkdir -p _test_data
pushd _test_data

    # Basic key handling

    mkdir -p keystore
    cp ../tests/data/alice.key keystore
    cp ../tests/data/bob.key keystore
    aut list accounts --keystore keystore > accounts
    [ 2 == $(wc -l < accounts) ] || (echo "unexpected number of accounts"; exit 1)

    # List account info
    aut get account --stdin < accounts

    # Remove WEB3_ENDPOINT env var and set up a configuration file instead
    unset WEB3_ENDPOINT

    echo '[aut]' > .autrc
    echo 'rpc_endpoint = https://rpc1.piccadilly.autonity.org:8545/' >> .autrc
    echo 'keyfile = keystore/alice.key' >> .autrc

    # Get Alice and Bob's balances
    alice_balance_orig=`aut get balance $ALICE`
    bob_balance_orig=`aut get balance $BOB`

    # Fake NTN transfer transaction.  Specify everything, to avoid
    # web3.py querying the node (which fails if ALICE has insufficient
    # NTN).
    aut --verbose maketx \
        --ntn \
        --from ${BOB} \
        --to ${ALICE} \
        --value '0.002kwei' \
        --gas 1000000 \
        --gas-price 1000000000 \
        --nonce 12 > test_ntn_tx

    # Sign the tx using Bobs private key
    KEYFILEPWD=bob aut --verbose signtx --key-file keystore/bob.key test_ntn_tx > test_ntn_tx.signed

    # TODO: Send the above when we can fund dummy accounts with NTN

    # Tiny send tx from Alice to Bob.  Extract Alice's address from
    # the keyfile given in .autrc
    aut --verbose maketx \
        --to ${BOB} \
        --value '0.001kwei' \
        --gas-price 1000000000 > test_tx

    # Sign the tx using Alices private key (taken from the .autrc file)
    KEYFILEPWD=alice aut --verbose signtx test_tx > test_tx.signed

    # Send the transaction
    aut sendtx test_tx.signed > test_tx.hash

    # Wait for transaction
    aut waittx `cat test_tx.hash`

    # Check Bob's new balances is 1 greater than the starting balance
    bob_balance_new=`aut get balance $BOB`
    [ "${bob_balance_new}" == "$((${bob_balance_orig} + 1))" ] || (
        echo "Unexpected balance change"; exit 1)

    popd
