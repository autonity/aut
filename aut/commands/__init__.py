from click import group

from aut.lazy_loading import LazyGroup


@group(
    name="account",
    cls=LazyGroup,
    subcommands={
        "list": "account.list_cmd",
        "info": "account.info",
        "balance": "account.balance",
        "lntn-balances": "account.lntn_balances",
        "new": "account.new",
        "import-private-key": "account.import_private_key",
        "signtx": "account.signtx",
        "sign-message": "account.sign_message",
        "verify-signature": "account.verify_signature",
    })
def account_group() -> None:
    """
    Commands related to specific accounts.
    """


@group(
    name="block",
    cls=LazyGroup,
    subcommands={
        "get": "block.get",
        "height": "block.height",
    })
def block_group() -> None:
    """
    Commands for querying block information.
    """


@group(name="contract")
def contract_group() -> None:
    """
    Command for interacting with arbitrary contracts.
    """


@group(name="node")
def node_group() -> None:
    """
    Commands related to querying specific Autonity nodes.
    """


@group(name="protocol")
def protocol_group() -> None:
    """
    Commands related to Autonity-specific protocol operations.  See
    the Autonity contract reference for details.
    """


@group(name="token")
def token_group() -> None:
    """
    Commands for working with ERC20 tokens.
    """


@group(
    name="tx",
    cls=LazyGroup,
    lazy_subcommands={
        # Re-use the `account signtx` command as `tx sign`
        "sign": "account.signtx",
    })
def tx_group() -> None:
    """
    Commands for transaction creation and processing.
    """


@group(
    name="validator",
    lazy_subcommands={
        # Re-use the `protocol get-validators` command as `validator list`
        "list": "protocol.get_validators",
    })
def validator_group() -> None:
    """
    Commands related to the validators.
    """
