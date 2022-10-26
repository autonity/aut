#!/usr/bin/env bash

set -x
set -e

# Test assumes a live testnet, and relies on Alice having some funds.
# Got to: https://faucet.autonity.org/ to recharge.
export WEB3_ENDPOINT="https://rpc1.piccadilly.autonity.org:8545/"

# We use these dummy Dummy keys:
ALICE=0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf
BOB=0x2B5AD5c4795c026514f8317c7a215E218DcCD6cF
CAROL=0x6813Eb9362372EEF6200f3b1dbC3f819671cBA69

# TODO: Get Alice and Bob's balances
# aut balance ${ALICE}

# Tiny send tx from 1 to 2
aut maketx \
    --from ${ALICE} \
    --to ${BOB} \
    --value '1wei' \
    --gas 3000000 --gas-price 1000000000 > test.tx

# Sign the tx using Alices private key
KEYFILEPWD=alice aut signtx --key-file tests/data/alice.key test.tx > test.signed.tx

# Send the transaction
aut sendtx test.signed.tx

# TODO: Wait for transaction

# TODO: check Alice and Bob's new balances
