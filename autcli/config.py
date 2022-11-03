"""
Configuration-related code
"""

from autcli.config_file import get_config_file, CONFIG_FILE_NAME

import os
from click import ClickException
from getpass import getpass
from typing import Optional


DEFAULT_KEYFILE_DIRECTORY = "~/.autonity/keystore"
KEYFILE_DIRECTORY_ENV_VAR = "~/.autonity/keystore"
KEYFILE_ENV_VAR = "KEYFILE"
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
            keystore_directory = get_config_file().get_path("keystore")
            if keystore_directory is None:
                keystore_directory = DEFAULT_KEYFILE_DIRECTORY

    assert keystore_directory is not None
    return keystore_directory


def get_keyfile_optional(keyfile: Optional[str]) -> Optional[str]:
    """
    Get the keyfile configuration if available.
    """
    if keyfile is None:
        keyfile = os.getenv(KEYFILE_ENV_VAR)
        if keyfile is None:
            keyfile = get_config_file().get_path("keyfile")

    return keyfile


def get_keyfile(keyfile: Optional[str]) -> str:
    """
    Get the keyfile configuration, raising a Click error if not given.
    """
    keyfile = get_keyfile_optional(keyfile)
    if keyfile is None:
        raise ClickException(
            f"No keyfile specified (use --key-file, {KEYFILE_ENV_VAR} env var "
            f"or {CONFIG_FILE_NAME})"
        )

    return keyfile


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
            endpoint = get_config_file().get("rpc_endpoint")
            if endpoint is None:
                raise ClickException(
                    f"No RPC endpoint given (use --rpc-endpoint, {WEB3_ENDPOINT_ENV_VAR}"
                    f"env var or {CONFIG_FILE_NAME})"
                )

    return endpoint
