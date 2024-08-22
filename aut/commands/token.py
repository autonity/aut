"""
The `token` command group.
"""

from typing import Optional

from autonity.erc20 import ERC20
from autonity.utils.denominations import format_quantity
from click import ClickException, argument, command, group
from eth_typing import ChecksumAddress
from web3 import Web3
from web3.types import Wei

from ..options import (
    config_option,
    keyfile_option,
    keyfile_or_from_option,
    newton_or_token_option,
    rpc_endpoint_option,
    tx_aux_options,
)
from ..param_types import ChecksumAddressType, TokenValueType
from ..utils import (
    create_contract_tx_from_args,
    from_address_from_argument,
    newton_or_token_to_address_require,
    parse_token_value_representation,
    to_json,
)

# pylint: disable=too-many-locals
# pylint: disable=too-many-arguments


@group(name="token")
def token_group() -> None:
    """Commands for working with ERC20 tokens."""


@command()
@config_option
@rpc_endpoint_option
@newton_or_token_option
def name(w3: Web3, ntn: bool, token: Optional[ChecksumAddress]) -> None:
    """Returns the token name (if available)."""

    token_addresss = newton_or_token_to_address_require(ntn, token)
    erc = ERC20(w3, token_addresss)
    token_name = erc.name()
    if token_name is None:
        raise ValueError("Token does not implement the name call")
    print(token_name)


token_group.add_command(name)


@command()
@config_option
@rpc_endpoint_option
@newton_or_token_option
def symbol(w3: Web3, ntn: bool, token: Optional[ChecksumAddress]) -> None:
    """Returns the token symbol (if available)."""

    token_addresss = newton_or_token_to_address_require(ntn, token)
    erc = ERC20(w3, token_addresss)
    token_symbol = erc.symbol()
    if token_symbol is None:
        raise ClickException("Token does not implement the symbol call")
    print(token_symbol)


token_group.add_command(symbol)


@command()
@config_option
@rpc_endpoint_option
@newton_or_token_option
def decimals(w3: Web3, ntn: bool, token: Optional[ChecksumAddress]) -> None:
    """Returns the number of decimals used in the token balances."""

    token_addresss = newton_or_token_to_address_require(ntn, token)
    erc = ERC20(w3, token_addresss)
    print(erc.decimals())


token_group.add_command(decimals)


@command()
@config_option
@rpc_endpoint_option
@newton_or_token_option
def total_supply(w3: Web3, ntn: bool, token: Optional[ChecksumAddress]) -> None:
    """Total supply (in units of whole Tokens)."""

    token_addresss = newton_or_token_to_address_require(ntn, token)
    erc = ERC20(w3, token_addresss)
    token_decimals = erc.decimals()
    token_total_supply = erc.total_supply()
    print(format_quantity(token_total_supply, token_decimals))


token_group.add_command(total_supply)


@command()
@config_option
@rpc_endpoint_option
@newton_or_token_option
@keyfile_option()
@argument("account", type=ChecksumAddressType(), required=False)
def balance_of(
    w3: Web3,
    ntn: bool,
    token: Optional[ChecksumAddress],
    keyfile: Optional[str],
    account: Optional[ChecksumAddress],
) -> None:
    """Returns the balance in tokens of an account.

    If ACCOUNT is not specified, the default keyfile is used.
    """

    token_addresss = newton_or_token_to_address_require(ntn, token)
    account_addr = from_address_from_argument(account, keyfile)

    erc = ERC20(w3, token_addresss)
    balance = erc.balance_of(account_addr)
    token_decimals = erc.decimals()
    print(format_quantity(balance, token_decimals))


token_group.add_command(balance_of)


@command()
@config_option
@rpc_endpoint_option
@newton_or_token_option
@keyfile_or_from_option
@argument("owner", type=ChecksumAddressType())
def allowance(
    w3: Web3,
    ntn: bool,
    token: Optional[ChecksumAddress],
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    owner: ChecksumAddress,
) -> None:
    """Returns the quantity in tokens that an owner has granted the caller permission
    to spend.

    The caller is the "from" address.
    """

    token_addresss = newton_or_token_to_address_require(ntn, token)
    from_addr = from_address_from_argument(from_, keyfile)

    erc = ERC20(w3, token_addresss)
    token_allowance = erc.allowance(owner, from_addr)
    token_decimals = erc.decimals()
    print(format_quantity(token_allowance, token_decimals))


token_group.add_command(allowance)


@command()
@config_option
@rpc_endpoint_option
@newton_or_token_option
@keyfile_or_from_option
@tx_aux_options
@argument("recipient", type=ChecksumAddressType())
@argument("amount_str", metavar="AMOUNT")
def transfer(
    w3: Web3,
    ntn: bool,
    token: Optional[ChecksumAddress],
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    recipient: ChecksumAddress,
    amount_str: str,
) -> None:
    """
    Create a transaction transferring tokens to a recipient.

    AMOUNT may be fractional if the token supports it.
    """

    token_address = newton_or_token_to_address_require(ntn, token)
    from_addr = from_address_from_argument(from_, keyfile)

    erc = ERC20(w3, token_address)

    token_decimals = erc.decimals()
    amount = parse_token_value_representation(amount_str, token_decimals)

    function_call = erc.transfer(recipient, amount)
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
@config_option
@rpc_endpoint_option
@newton_or_token_option
@keyfile_or_from_option
@tx_aux_options
@argument("spender", type=ChecksumAddressType())
@argument("amount_str", metavar="AMOUNT")
def approve(
    w3: Web3,
    ntn: bool,
    token: Optional[ChecksumAddress],
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    spender: ChecksumAddress,
    amount_str: str,
) -> None:
    """Create a transaction granting a spender permission to spend tokens.

    The tokens are owned by the `--from` account. AMOUNT may be
    fractional if the token supports it.
    """

    token_addresss = newton_or_token_to_address_require(ntn, token)
    from_addr = from_address_from_argument(from_, keyfile)

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
@config_option
@rpc_endpoint_option
@newton_or_token_option
@keyfile_or_from_option
@tx_aux_options
@argument("spender", type=ChecksumAddressType())
@argument("recipient", type=ChecksumAddressType())
@argument("amount_str", metavar="AMOUNT")
def transfer_from(
    w3: Web3,
    ntn: bool,
    token: Optional[ChecksumAddress],
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    spender: ChecksumAddress,
    recipient: ChecksumAddress,
    amount_str: str,
) -> None:
    """Create a transaction transferring tokens.

    Tokens held by SPENDER are transferred to RECIPIENT.
    SPENDER must previously have granted the caller (`--from` account) permission to
    spend these tokens, via an `approve` transaction.
    AMOUNT can be fractional if the token supports it.
    """

    token_addresss = newton_or_token_to_address_require(ntn, token)
    from_addr = from_address_from_argument(from_, keyfile)

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
