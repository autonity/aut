# Autonity CLI

A command-line RPC client for Autonity.  Run `aut --help` for the list of all commands and options.

## Quick Start

Requirements:
- Python 3.8 or 3.9 (at the time of writing, 3.10+ is incompatible with the latest stable version of the `web3.py` dependency)
- a recent version of [pipx](https://pypa.github.io/pipx/)

The `aut` tool can then be installed as a pipx package isolated in its own environment:
```console
$ pipx install https://github.com/autonity/autcli.git
```

**Note:** Until they are made public, you will need sufficient credentials to access the above repository.  If you don't have `https` tokens, you may need to use the SSH-style url:
```console
$ pipx install git+ssh://git@github.com/autonity/autcli.git
```
If you are trying to install on a VPS, or other machine without github credentials, you may need to [set these up](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) for that host.

**Note:** If you need to specify a specific python version (because pipx selects a version that is not compatible with `autcli`), use the `--python` flag `pipx install --python $(which python3.9) <url>`.  See the `pipx install` help text for details.  If your system does not have a supported version of python, install one using the package manager for your OS, or using [pyenv](https://github.com/pyenv/pyenv).

Once successfully installed, the `aut` command should be available in the PATH.  All commands are discoverable from the help text.  Type `aut --help`, `aut <command> --help` etc. for details.

## (Optional) Enable command completion (bash and zsh)

Completion is available in `bash` and `zsh` shells as follows.  (Adapt these commands to your particular configuration.)

```console
# For zsh, replace bash_source with zsh_source.
$ _AUT_COMPLETE=bash_source aut > ~/.aut-complete
$ echo 'source ~/.aut-complete' >> ~/.bashrc
```
Auto-complete should be enabled in new shells.

## `.autrc` files

If the `aut` command find this file, it reads configuration parameters from it.  See the [sample file](.autrc.sample) in this repo.  This avoids the need to enter certain values on the command line. These parameters can be overridden by environment variables and command-line parameters where necessary.

If `.autrc` is not found in the current directory, all parent directories are searched in turn and the first `.autrc` file found is used.  Alternatively, this file can be placed in `~/.config/aut/autrc`.

A very simple `.autrc` file may specify the endpoint for Web3 connections:
```console
# Create a config file holding the rpc endpoint.
$ echo '[aut]' > .autrc
$ echo 'rpc_endpoint = https://rpc1.piccadilly.autonity.org:8545/' >> .autrc
```

## Usage Examples

### Create a new account (for demo purposes)

```console
# Create an account
# !! For demonstration purposes only. Use a HW wallet or other key-management infrastructure. !!
$ mkdir -p keystore
$ aut account new --key-file keystore/alice.key
Password for new account:
Confirm account password:
0xd888bc90720757796C72eC2a3A231c81b55e8097
```

This can be added as the default key for transaction signing (and default address for queries) in the `.autrc` file:

```console
$ echo 'keyfile = keystore/alice.key' >> .autrc
```

### Check account balance (after funding the account)

```console
# Check Alice's balance (use address in keystore/alice.key), given in Wei.
$ aut account balance
100000000000000000000
# Check Bob's balance (1 XTN).  Bob's address is 0x4EcE2e62E67a7B64a83D3E180dC86962145b762f
$ aut account balance 0x4EcE2e62E67a7B64a83D3E180dC86962145b762f
1000000000000000000
```

### Create, sign and send a transaction

```console
# Send 1 XTN to Bob
$ aut tx make --to 0x4EcE2e62E67a7B64a83D3E180dC86962145b762f --value 1aut | aut tx sign - | aut tx send -
Enter passphrase (or CTRL-d to exit):
0x47f71a94372d00a3066414b80f3b9c78d71b3011479ddc86e37ab86e0fe80d8a
```

Explanation of the above: The `maketx` command extracts the `from` address from the default keyfile, and automatically sets the `gas`, `nonce` and other fields by querying the RPC endpoint in the config file.  It then writes this to `stdout`, which is piped to the `signtx` command, using the `-` argument to indicate `stdin`.  The sign `signtx` decrypts the default keyfile after querying the user for the password, and writes the signed transaction to `stdout`.  This is then piped to the `sendtx` command, which connects to the RPC endpoint given in the config file and passes the signed transaction to the node for broadcast.  `sendtx` then outputs the transaction hash to `stdout`.

All configuration options can be set using command-line parameters to override the configuration file. Use the `--help` flag with any command to see all available options.

### Wait for the transaction

```console
# Wait for a transaction to complete.  Print the transaction receipt to stdout.
$ aut tx wait 0x47f71a94372d00a3066414b80f3b9c78d71b3011479ddc86e37ab86e0fe80d8a
{"blockHash": "0x65e74faaaee5efa3b6e998fd78c8e1ca3085c8bd88709101e8fa801a03ab371d", "blockNumber": 5780419, "contractAddress": null, "cumulativeGasUsed": 21000, "effectiveGasPrice": 1000000000, "from": "0xd888bc90720757796C72eC2a3A231c81b55e8097", "gasUsed": 21000, "logs": [], "logsBloom": "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000", "status": 1, "to": "0x4EcE2e62E67a7B64a83D3E180dC86962145b762f", "transactionHash": "0x47f71a94372d00a3066414b80f3b9c78d71b3011479ddc86e37ab86e0fe80d8a", "transactionIndex": 0, "type": "0x2"}

# Re-check Bob's balance
$ aut account balance 0x4EcE2e62E67a7B64a83D3E180dC86962145b762f
2000000000000000000
```

## Development

The [autonity.py](https://github.com/autonity/autonity.py) dependency
is included as a submodule, for ease of development.  Sync all submodules, e.g.:
```console
$ git submodule update --init --recursive
```

Create and activate a virtual-env for development:
```console
$ python -m venv env
$ . env/bin/activate
```

(Note the `(env)` prefix to your prompt.  Activate the venv from other
terminals using the same `. env/bin/activate` command.)

Install both `autetl` and `autonity.py` in "editable" mode, within this virtual-env:
development:
```console
(env)$ make
```

(Note that the `aut` command is also installed in the virtual-env.)

To run all code checks (linters, type-checker, unit tests, etc):
```console
(env)$ make check
```

Several tests scripts (which invoke the `aut` command itself) are available in the [scripts](./scripts) directory.  The are intended to be run within the Python virtual-env, from the repository root directory.
