"""
Code that is executed when 'aut list..' is invoked on the command-line.
"""
from docopt import docopt
from autcli.constants import UnixExitStatus
from autcli.utils import address_keyfile_dict
from autcli import __version__
from autcli import __file__
from schema import Schema, SchemaError, Or, Use
import sys
import os
import glob
import autcli


def aut_list(argv):
    """
    Usage:
      aut list <command> [options]

    Commands:
      commands
      accounts

    Options:
      --with-files      also show keyfile names.
      --keystore=<DIR>  local keystore directory [default: ~/.autonity/keystore].
      --debug           if set, errors will print traceback along with exception msg.
      -h --help         show this screen.
    """
    try:
        args = docopt(aut_list.__doc__, version=__version__, argv=argv)
    except:
        print(aut_list.__doc__)
        return UnixExitStatus.CLI_INVALID_INVOCATION
    if not args["--debug"]:
        sys.tracebacklimit = 0
    del args["list"]
    s = Schema(
        {
            "--keystore": Or(None, Use(os.path.expanduser)),
            "--with-files": Or(True, False),
            "--debug": Or(True, False),
            "--help": Or(True, False),
            "<command>": Or(
                "commands",
                "accounts",
                error="<command> must be 'commands' or 'accounts'",
            ),
        }
    )
    try:
        args = s.validate(args)
    except SchemaError as exc:
        print(exc.code)
        return UnixExitStatus.CLI_INVALID_OPTION_VALUE
    if args["<command>"] == "accounts":
        keyfiles = address_keyfile_dict(args["--keystore"])
        for addr in keyfiles.keys():
            if args["--with-files"]:
                print(addr + " " + keyfiles[addr])
            else:
                print(addr)
    elif args["<command>"] == "commands":
        pkg_path = os.path.dirname(autcli.__file__)
        cmd_paths = glob.glob(pkg_path + "/commands/" + "[a-z]*.py")
        cmd_paths.sort()
        for p in cmd_paths:
            f = os.path.basename(p)
            cmd_name = os.path.splitext(f)[0]
            if args["--with-files"]:
                print(cmd_name + " " + p)
            else:
                print(cmd_name)
    return 0
