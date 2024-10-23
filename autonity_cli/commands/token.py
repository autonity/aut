"""
The `token` command group.
"""

from typing import Optional

from click import ClickException, argument, command, group

from ..options import (
    from_option,
    keyfile_option,
    newton_or_token_option,
    rpc_endpoint_option,
    tx_aux_options,
)

# Disable pylint warning about imports outside top-level.  We do this
# intentionally to try and keep startup times of the CLI low.

# pylint: disable=import-outside-toplevel
# pylint: disable=too-many-locals
# pylint: disable=too-many-arguments


@group(name="token")
def token_group() -> None:
    """
    Commands for working with ERC20 tokens.
    """


@command()
@rpc_endpoint_option
@newton_or_token_option
def name(rpc_endpoint: Optional[str], ntn: bool, token: Optional[str]) -> None:
    """
    Returns the token name (if available).
    """

    from autonity.erc20 import ERC20

    from ..utils import (
        newton_or_token_to_address_require,
        web3_from_endpoint_arg,
    )

    token_addresss = newton_or_token_to_address_require(ntn, token)
    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    erc = ERC20(w3, token_addresss)
    token_name = erc.name()
    if token_name is None:
        raise ValueError("Token does not implement the name call")
    print(token_name)


token_group.add_command(name)


@command()
@rpc_endpoint_option
@newton_or_token_option
def symbol(rpc_endpoint: Optional[str], ntn: bool, token: Optional[str]) -> None:
    """
    Returns the token symbol (if available).
    """

    from autonity.erc20 import ERC20

    from ..utils import (
        newton_or_token_to_address_require,
        web3_from_endpoint_arg,
    )

    token_addresss = newton_or_token_to_address_require(ntn, token)
    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    erc = ERC20(w3, token_addresss)
    token_symbol = erc.symbol()
    if token_symbol is None:
        raise ClickException("Token does not implement the symbol call")
    print(token_symbol)


token_group.add_command(symbol)


@command()
@rpc_endpoint_option
@newton_or_token_option
def decimals(rpc_endpoint: Optional[str], ntn: bool, token: Optional[str]) -> None:
    """
    Returns the number of decimals used in the token balances.
    """

    from autonity.erc20 import ERC20

    from ..utils import (
        newton_or_token_to_address_require,
        web3_from_endpoint_arg,
    )

    token_addresss = newton_or_token_to_address_require(ntn, token)
    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    erc = ERC20(w3, token_addresss)
    print(erc.decimals())


token_group.add_command(decimals)


@command()
@rpc_endpoint_option
@newton_or_token_option
def total_supply(rpc_endpoint: Optional[str], ntn: bool, token: Optional[str]) -> None:
    """
    Total supply (in units of whole Tokens).
    """
    from autonity.erc20 import ERC20
    from autonity.utils.denominations import format_quantity

    from ..utils import (
        newton_or_token_to_address_require,
        web3_from_endpoint_arg,
    )

    token_addresss = newton_or_token_to_address_require(ntn, token)
    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    erc = ERC20(w3, token_addresss)
    token_decimals = erc.decimals()
    token_total_supply = erc.total_supply()
    print(format_quantity(token_total_supply, token_decimals))


token_group.add_command(total_supply)


@command()
@rpc_endpoint_option
@newton_or_token_option
@keyfile_option()
@argument("account_str", metavar="ACCOUNT", required=False)
def balance_of(
    rpc_endpoint: Optional[str],
    ntn: bool,
    token: Optional[str],
    keyfile: Optional[str],
    account_str: Optional[str],
) -> None:
    """
    Returns the balance in tokens of ACCOUNT.  If ACCOUNT is not
    specified, the default keyfile is used.
    """

    from autonity.erc20 import ERC20
    from autonity.utils.denominations import format_quantity

    from ..utils import (
        from_address_from_argument,
        newton_or_token_to_address_require,
        web3_from_endpoint_arg,
    )

    token_addresss = newton_or_token_to_address_require(ntn, token)
    account_addr = from_address_from_argument(account_str, keyfile)

    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    erc = ERC20(w3, token_addresss)
    balance = erc.balance_of(account_addr)
    token_decimals = erc.decimals()
    print(format_quantity(balance, token_decimals))


token_group.add_command(balance_of)


@command()
@rpc_endpoint_option
@newton_or_token_option
@keyfile_option()
@from_option
@argument("owner")
def allowance(
    rpc_endpoint: Optional[str],
    ntn: bool,
    token: Optional[str],
    keyfile: Optional[str],
    from_str: Optional[str],
    owner: str,
) -> None:
    """
    Returns the quantity in tokens that OWNER has granted the caller
    (the "from" address) permission to spend.
    """
    from autonity.erc20 import ERC20
    from autonity.utils.denominations import format_quantity
    from web3 import Web3

    from ..utils import (
        from_address_from_argument,
        newton_or_token_to_address_require,
        web3_from_endpoint_arg,
    )

    token_addresss = newton_or_token_to_address_require(ntn, token)
    from_addr = from_address_from_argument(from_str, keyfile)
    owner_addr = Web3.to_checksum_address(owner)

    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    erc = ERC20(w3, token_addresss)
    token_allowance = erc.allowance(owner_addr, from_addr)
    token_decimals = erc.decimals()
    print(format_quantity(token_allowance, token_decimals))


token_group.add_command(allowance)


@command()
@rpc_endpoint_option
@newton_or_token_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("recipient_str", metavar="RECIPIENT")
@argument("amount_str", metavar="AMOUNT")
def transfer(
    rpc_endpoint: Optional[str],
    ntn: bool,
    token: Optional[str],
    keyfile: Optional[str],
    from_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    recipient_str: str,
    amount_str: str,
) -> None:
    """
    Create a transaction transferring AMOUNT of tokens to RECIPIENT.  AMOUNT may
    be fractional if the token supports it.
    """

    from autonity.erc20 import ERC20
    from web3 import Web3

    from ..utils import (
        create_contract_tx_from_args,
        from_address_from_argument,
        newton_or_token_to_address_require,
        parse_token_value_representation,
        to_json,
        web3_from_endpoint_arg,
    )

    token_addresss = newton_or_token_to_address_require(ntn, token)
    from_addr = from_address_from_argument(from_str, keyfile)
    recipient_addr = Web3.to_checksum_address(recipient_str)

    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    erc = ERC20(w3, token_addresss)

    token_decimals = erc.decimals()
    amount = parse_token_value_representation(amount_str, token_decimals)

    function_call = erc.transfer(recipient_addr, amount)
    tx = create_contract_tx_from_args(
        function=function_call,
        from_addr=from_addr,
        gas=gas,
        gas_price=gas_price,
        max_fee_per_gas=max_fee_per_gas,
        max_priority_fee_per_gas=max_priority_fee_per_gas,
        fee_factor=fee_factor,
        nonce=nonce,
        chain_id=chain_id,
    )

    print(to_json(tx))


token_group.add_command(transfer)


@command()
@rpc_endpoint_option
@newton_or_token_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("spender_str", metavar="SPENDER")
@argument("amount_str", metavar="AMOUNT")
def approve(
    rpc_endpoint: Optional[str],
    ntn: bool,
    token: Optional[str],
    keyfile: Optional[str],
    from_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    spender_str: str,
    amount_str: str,
) -> None:
    """
    Create a transaction granting SPENDER permission to spend
    AMOUNT of tokens owned by `from_addr`.  AMOUNT may be
    fractional if the token supports it.
    """

    from autonity.erc20 import ERC20
    from web3 import Web3

    from ..utils import (
        create_contract_tx_from_args,
        from_address_from_argument,
        newton_or_token_to_address_require,
        parse_token_value_representation,
        to_json,
        web3_from_endpoint_arg,
    )

    token_addresss = newton_or_token_to_address_require(ntn, token)
    from_addr = from_address_from_argument(from_str, keyfile)
    spender = Web3.to_checksum_address(spender_str)

    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    erc = ERC20(w3, token_addresss)

    token_decimals = erc.decimals()
    amount = parse_token_value_representation(amount_str, token_decimals)

    function_call = erc.approve(spender, amount)
    tx = create_contract_tx_from_args(
        function=function_call,
        from_addr=from_addr,
        gas=gas,
        gas_price=gas_price,
        max_fee_per_gas=max_fee_per_gas,
        max_priority_fee_per_gas=max_priority_fee_per_gas,
        fee_factor=fee_factor,
        nonce=nonce,
        chain_id=chain_id,
    )

    print(to_json(tx))


token_group.add_command(approve)


@command()
@rpc_endpoint_option
@newton_or_token_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("spender_str", metavar="SPENDER")
@argument("recipient_str", metavar="RECIPIENT")
@argument("amount_str", metavar="AMOUNT")
def transfer_from(
    rpc_endpoint: Optional[str],
    ntn: bool,
    token: Optional[str],
    keyfile: Optional[str],
    from_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    spender_str: str,
    recipient_str: str,
    amount_str: str,
) -> None:
    """
    Create a transaction transferring AMOUNT of tokens held by SPENDER
    to RECIPIENT.  SPENDER must previously have granted the caller
    (`from_addr`) permission to spend these tokens, via an `approve`
    transaction.  AMOUNT can be fractional if the token supports it.
    """

    from autonity.erc20 import ERC20
    from web3 import Web3

    from ..utils import (
        create_contract_tx_from_args,
        from_address_from_argument,
        newton_or_token_to_address_require,
        parse_token_value_representation,
        to_json,
        web3_from_endpoint_arg,
    )

    token_addresss = newton_or_token_to_address_require(ntn, token)
    from_addr = from_address_from_argument(from_str, keyfile)
    spender = Web3.to_checksum_address(spender_str)
    recipient = Web3.to_checksum_address(recipient_str)

    w3 = web3_from_endpoint_arg(None, rpc_endpoint)
    erc = ERC20(w3, token_addresss)

    token_decimals = erc.decimals()
    amount = parse_token_value_representation(amount_str, token_decimals)

    function_call = erc.transfer_from(spender, recipient, amount)
    tx = create_contract_tx_from_args(
        function=function_call,
        from_addr=from_addr,
        gas=gas,
        gas_price=gas_price,
        max_fee_per_gas=max_fee_per_gas,
        max_priority_fee_per_gas=max_priority_fee_per_gas,
        fee_factor=fee_factor,
        nonce=nonce,
        chain_id=chain_id,
    )

    print(to_json(tx))


token_group.add_command(transfer_from)
