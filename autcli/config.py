"""
Configuration-related code
"""

import os
from click import ClickException
from getpass import getpass
from typing import Optional


DEFAULT_KEYFILE_DIRECTORY = "~/.autonity/keystore"
KEYFILE_DIRECTORY_ENV_VAR = "~/.autonity/keystore"
KEYFILE_PASSWORD_ENV_VAR = "KEYFILEPWD"
WEB3_ENDPOINT_ENV_VAR = "WEB3_ENDPOINT"


def get_keystore_directory(keystore_directory: Optional[str]) -> str:
    """
    Get the keystore directory.  In order, use the command-line
    parameter, falling back to the env var then config file, and finally to
    DEFAULT_KEYFILE_DIRECTORY.
    """
    if keystore_directory is None:
        keystore_directory = os.getenv(KEYFILE_DIRECTORY_ENV_VAR)
        if keystore_directory is None:
            # TODO: read from config file
            keystore_directory = DEFAULT_KEYFILE_DIRECTORY

    assert keystore_directory is not None
    return keystore_directory


def get_keyfile_password(
    password: Optional[str], key_file: Optional[str] = None
) -> str:
    """
    Get the keyfile password, given a cli parameter `password`.  Fall
    back to env vars if cli parameter is not given, then to user
    input.
    """

    # Read password
    if password is None:
        password = os.getenv(KEYFILE_PASSWORD_ENV_VAR)
        if password is None:
            password = getpass(
                "KEYFILEPWD env var not set (consider using 'KEYFILEPWD').\n"
                + "Enter passphrase "
                + ("" if key_file is None else f"for {key_file} ")
                + "(or CTRL-d to exit): "
            )

    return password


def get_rpc_endpoint(endpoint: Optional[str]) -> str:
    """
    Get the RPC endpoint configuration value, where param is the
    command-line option. If param is not given, check the env var,
    then configuration files, falling back to the default.
    """

    if endpoint is None:
        endpoint = os.getenv(WEB3_ENDPOINT_ENV_VAR)
        if endpoint is None:
            raise ClickException(
                f"No RPC endpoint given (use --rpc-endpoint or {WEB3_ENDPOINT_ENV_VAR} env var)"
            )

    return endpoint
