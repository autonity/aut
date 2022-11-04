"""
Configuration file definition
"""

from __future__ import annotations

from autcli.logging import log

import os
import os.path
from configparser import ConfigParser
from typing import Mapping, Optional, Any

# pylint: disable=global-statement


class ConfigFile:
    """
    Wrap a config file section, adding the ability to query a relative path
    """

    _section: Mapping[str, Any]

    def __init__(self, section: Mapping[str, Any]):
        self._section = section

    def get(self, attribute: str) -> Optional[str]:
        """
        String attribute
        """
        return self._section.get(attribute)

    def get_path(self, attribute: str) -> Optional[str]:
        """
        Return the full path of an attribute specified relative to the
        config file.  E.e. if config file at ../.autrc contains
        somedir/somefile, return ../somedir/somefile.
        """
        attr_path = self._section.get(attribute)
        if attr_path:
            return os.path.normpath(os.path.join(CONFIG_FILE_DIR, attr_path))

        return None


CONFIG_FILE_NAME = ".autrc"

CONFIG_FILE_SECTION_NAME = "aut"

CONFIG_FILE_DATA: ConfigFile = ConfigFile({})

CONFIG_FILE_DIR: str = "."

CONFIG_FILE_CACHED = False


def _find_config_file() -> str | None:
    """
    Find the config file in the file system.  For now, find the first
    .autrc file in the current or any parent dir.
    """

    # Start at
    cur_dir = os.getcwd()

    while True:
        config_path = os.path.join(cur_dir, CONFIG_FILE_NAME)
        if os.path.exists(config_path):
            log(f"found config file: {config_path}")
            return config_path

        parent_dir = os.path.normpath(os.path.join(cur_dir, ".."))
        if parent_dir == cur_dir:
            log(f"no {CONFIG_FILE_NAME} file found")
            break

        cur_dir = parent_dir

    return None


def get_config_file() -> ConfigFile:
    """
    Load (and cache in memory) the first config file found.  If no
    config file is found, the empty dictionary is returned.
    """

    global CONFIG_FILE_DIR
    global CONFIG_FILE_DATA
    global CONFIG_FILE_CACHED

    if not CONFIG_FILE_CACHED:
        config_file_path = _find_config_file()
        if config_file_path:
            config = ConfigParser()
            config.read(config_file_path)
            CONFIG_FILE_DIR = os.path.dirname(config_file_path)
            CONFIG_FILE_DATA = ConfigFile(config[CONFIG_FILE_SECTION_NAME])

        CONFIG_FILE_CACHED = True

    return CONFIG_FILE_DATA
