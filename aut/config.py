"""
Configuration-related code. Determines precedence of command
line, config and defaults, and handles extracting from the config
file.
"""

import os
from configparser import ConfigParser
from typing import Any, Dict, Optional

from click import Context

from .logging import log


CONFIG_FILE_NAME = "autrc"
CONFIG_SECTION_NAME = "aut"
ENV_VAR_PREFIX = "AUT_"
OPTION_ALIASES = {
    "abi": "contract_abi_path",
    "address": "contract_address_str",
    "from": "from_str",
    "validator": "validator_addr_str",
}

_config: Optional[Dict[str, Any]] = None


def read_defaults_from_config(
    ctx: Context, _: str, config_file_path: Optional[str]
) -> None:
    """
    Load the first config file found and set its values as Click option defaults.
    """

    global _config

    if _config is None:
        if config_file_path:
            config_file = ConfigParser()
            config_file.read(config_file_path)
            try:
                _config = dict(config_file[CONFIG_SECTION_NAME])
            except KeyError:
                _config = {}
        else:
            _config = {}

        # Env vars have higher precedence than config file items
        for key, value in os.environ.items():
            if key.startswith(ENV_VAR_PREFIX):
                _config[key.replace(ENV_VAR_PREFIX, "").lower()] = value

        for name, alias in OPTION_ALIASES.items():
            if name in _config:
                _config[alias] = _config.pop(name)

    ctx.default_map = _config


def _find_config_file() -> Optional[str]:
    """
    Find the config file in the file system.  For now, find the first
    .autrc file in the current or any parent dir.
    """

    if config_path := os.getenv(ENV_VAR_PREFIX + "CONFIG"):
        return config_path

    home_dir = os.path.expanduser("~")
    cur_dir = os.getcwd()

    while True:
        config_path = os.path.join(cur_dir, f".{CONFIG_FILE_NAME}")
        if os.path.exists(config_path):
            log(f"found config file: {config_path}")
            return config_path

        # If/when we reach the home directory, check also for ~/.config/aut/autrc
        if cur_dir == home_dir:
            config_path = os.path.join(home_dir, ".config", "aut", CONFIG_FILE_NAME)
            if os.path.exists(config_path):
                log(f"HOME dir. found {config_path}")
                return config_path

            log(f"HOME dir. no file {config_path}")

        parent_dir = os.path.normpath(os.path.join(cur_dir, ".."))
        if parent_dir == cur_dir:
            log(f"reached root. no {CONFIG_FILE_NAME} file found")
            break

        cur_dir = parent_dir

    return None


config_file = _find_config_file()
