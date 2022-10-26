#!/usr/bin/env bash

set -x
set -e

# Dummy keys:
#
# 00..01: '0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf'
# 00..02: '0x2B5AD5c4795c026514f8317c7a215E218DcCD6cF'
# 00..03: '0x6813Eb9362372EEF6200f3b1dbC3f819671cBA69'

ALICE=0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf
BOB=0x2B5AD5c4795c026514f8317c7a215E218DcCD6cF
CAROL=0x6813Eb9362372EEF6200f3b1dbC3f819671cBA69

export WEB3_ENDPOINT="https://rpc1.piccadilly.autonity.org:8545/"

# TODO: Get Alice's balance
# aut balance ${ALICE}

# Tiny send tx from 1 to 2
aut maketx --from ${ALICE} --to ${BOB} --value '1kwei' \
  --gas 3000000 --gas-price 10000000000 > test.tx

# Sign the tx using Alices private key
KEYFILEPWD=alice aut signtx --key-file tests/data/alice.key test.tx > test.signed.tx

# Send the transaction
aut sendtx test.signed.tx
