"""
The "info" command group
"""


from click import group, command, echo


# Disable pylint warning about imports outside top-level.  We do this
# intentionally to try and keep startup times of the CLI low.

# pylint: disable=import-outside-toplevel


@group(name="info")
def info_group() -> None:
    """
    Commands for querying info information.
    """


@command()
def autonity_contract_version() -> None:
    """
    Print the git commit hash of the bundled Autonity contract.
    """
    from autonity import get_autonity_contract_version

    echo(get_autonity_contract_version())


info_group.add_command(autonity_contract_version)


@command()
def autonity_contract_src() -> None:
    """
    Print the source code URL of the bundled Autonity contract.
    """
    from autonity import get_autonity_contract_version

    _v_ = get_autonity_contract_version()
    echo(
        f"https://github.com/autonity/autonity/blob/{_v_}/autonity/solidity/contracts/Autonity.sol"
    )


info_group.add_command(autonity_contract_src)


@command()
def autonity_contract_abi_path() -> None:
    """
    Print the bundled Autonity contract's ABI path.
    """
    from autonity import get_autonity_contract_abi_path

    echo(get_autonity_contract_abi_path(), nl=False)


info_group.add_command(autonity_contract_abi_path)


@command()
def autonity_contract_address() -> None:
    """
    Print the default Autonity contract address.
    """
    from autonity import AUTONITY_CONTRACT_ADDRESS

    echo(AUTONITY_CONTRACT_ADDRESS, nl=False)


info_group.add_command(autonity_contract_address)
