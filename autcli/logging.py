"""
Logging-related functions.
"""

import sys

# pylint: disable=global-statement

LOGGING_ENABLED = False


def enable_logging() -> None:
    """
    Call to enable the log function.
    """
    global LOGGING_ENABLED
    LOGGING_ENABLED = True


def log(msg: str, no_newline: bool = False) -> None:
    """
    Log a message.  Currently just goes to stderr.
    """
    if LOGGING_ENABLED:
        sys.stderr.write(msg)
        if not no_newline and msg[-1] != "\n":
            sys.stderr.write("\n")
