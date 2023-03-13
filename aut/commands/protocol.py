"""
The `autonity` command group.
"""

from aut.options import (
    rpc_endpoint_option,
    keyfile_option,
    from_option,
    tx_aux_options,
)

# from autonity import Autonity

from click import group, command, argument
from typing import Sequence, Optional, Any

# Disable pylint warning about imports outside top-level.  We do this
# intentionally to try and keep startup times of the CLI low.

# pylint: disable=import-outside-toplevel
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals


@group(name="protocol")
def protocol_group() -> None:
    """
    Commands related to Autonity-specific protocol operations.  See
    the Autonity contract reference for details.
    """


def _show_sequence(value: Sequence[Any]) -> str:
    return "\n".join([str(v) for v in value])


def _show_json(value: Any) -> str:
    from aut.utils import to_json

    return to_json(value, pretty=True)


@command()
@rpc_endpoint_option
def commission_rate_precision(rpc_endpoint: Optional[str]) -> None:
    """
    Precision of validator commission rate values
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).commission_rate_precision())


protocol_group.add_command(commission_rate_precision)


@command()
@rpc_endpoint_option
def config(rpc_endpoint: Optional[str]) -> None:
    """
    Print the Autonity contract config
    """
    from aut.utils import autonity_from_endpoint_arg

    print(_show_json(autonity_from_endpoint_arg(rpc_endpoint).config()))


protocol_group.add_command(config)


@command()
@rpc_endpoint_option
def epoch_id(rpc_endpoint: Optional[str]) -> None:
    """
    ID of current epoch
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).epoch_id())


protocol_group.add_command(epoch_id)


@command()
@rpc_endpoint_option
def last_epoch_block(rpc_endpoint: Optional[str]) -> None:
    """
    Block number of the last epoch
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).last_epoch_block())


protocol_group.add_command(last_epoch_block)


@command()
@rpc_endpoint_option
def epoch_total_bonded_stake(rpc_endpoint: Optional[str]) -> None:
    """
    Total stake bonded this epoch
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).epoch_total_bonded_stake())


protocol_group.add_command(epoch_total_bonded_stake)


@command()
@rpc_endpoint_option
def total_redistributed(rpc_endpoint: Optional[str]) -> None:
    """
    Total fees redistributed
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).total_redistributed())


protocol_group.add_command(total_redistributed)


@command()
@rpc_endpoint_option
def epoch_reward(rpc_endpoint: Optional[str]) -> None:
    """
    Reward for this epoch
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).epoch_reward())


protocol_group.add_command(epoch_reward)


@command()
@rpc_endpoint_option
def tail_bonding_id(rpc_endpoint: Optional[str]) -> None:
    """Tail ID of bonding queue"""
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).tail_bonding_id())


protocol_group.add_command(tail_bonding_id)


@command()
@rpc_endpoint_option
def head_bonding_id(rpc_endpoint: Optional[str]) -> None:
    """
    Head ID of bonding queue
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).head_bonding_id())


protocol_group.add_command(head_bonding_id)


@command()
@rpc_endpoint_option
def tail_unbonding_id(rpc_endpoint: Optional[str]) -> None:
    """
    Tail ID of unbonding queue
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).tail_unbonding_id())


protocol_group.add_command(tail_unbonding_id)


@command()
@rpc_endpoint_option
def head_unbonding_id(rpc_endpoint: Optional[str]) -> None:
    """
    Head ID of unbonding queue
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).head_unbonding_id())


protocol_group.add_command(head_unbonding_id)


@command()
@rpc_endpoint_option
def deployer(rpc_endpoint: Optional[str]) -> None:
    """
    Contract deployer
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).deployer())


protocol_group.add_command(deployer)


@command()
@rpc_endpoint_option
def get_last_epoch_block(rpc_endpoint: Optional[str]) -> None:
    """
    Block of last epoch
    """
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_last_epoch_block())


protocol_group.add_command(get_last_epoch_block)


@command()
@rpc_endpoint_option
def get_version(rpc_endpoint: Optional[str]) -> None:
    """Contract version"""
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_version())


protocol_group.add_command(get_version)


@command()
@rpc_endpoint_option
def get_committee(rpc_endpoint: Optional[str]) -> None:
    """
    Get current committee"
    """
    from aut.utils import autonity_from_endpoint_arg

    print(_show_json(autonity_from_endpoint_arg(rpc_endpoint).get_committee()))


protocol_group.add_command(get_committee)


@command()
@rpc_endpoint_option
def get_validators(rpc_endpoint: Optional[str]) -> None:
    """Get current validators"""
    from aut.utils import autonity_from_endpoint_arg

    print(_show_sequence(autonity_from_endpoint_arg(rpc_endpoint).get_validators()))


protocol_group.add_command(get_validators)


@command()
@rpc_endpoint_option
def get_max_committee_size(rpc_endpoint: Optional[str]) -> None:
    """Maximum committee size"""
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_max_committee_size())


protocol_group.add_command(get_max_committee_size)


@command()
@rpc_endpoint_option
def get_committee_enodes(rpc_endpoint: Optional[str]) -> None:
    """Enodes in current committee"""
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_committee_enodes())


protocol_group.add_command(get_committee_enodes)


@command()
@rpc_endpoint_option
def get_minimum_base_fee(rpc_endpoint: Optional[str]) -> None:
    """Minimum base fee"""
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_minimum_base_fee())


protocol_group.add_command(get_minimum_base_fee)


@command()
@rpc_endpoint_option
def get_operator(rpc_endpoint: Optional[str]) -> None:
    """Contract operator"""
    from aut.utils import autonity_from_endpoint_arg

    print(autonity_from_endpoint_arg(rpc_endpoint).get_operator())


protocol_group.add_command(get_operator)


@command()
@rpc_endpoint_option
@argument("height", type=int, nargs=1)
@argument("round_", metavar="ROUND", type=int, nargs=1)
def get_proposer(rpc_endpoint: Optional[str], height: int, round_: int) -> None:
    """
    Proposer at the given height and round
    """
    from aut.utils import web3_from_endpoint_arg
    from autonity import Autonity

    aut = Autonity(web3_from_endpoint_arg(None, rpc_endpoint))
    print(aut.get_proposer(height, round_))


protocol_group.add_command(get_proposer)


@command()
@rpc_endpoint_option
@argument("start", type=int, nargs=1)
@argument("end", type=int, nargs=1)
def get_bonding_req(rpc_endpoint: Optional[str], start: int, end: int) -> None:
    """
    Get queued bonding information between start and end ids.
    """
    from aut.utils import web3_from_endpoint_arg
    from autonity import Autonity

    aut = Autonity(web3_from_endpoint_arg(None, rpc_endpoint))
    print(_show_json(aut.get_bonding_req(start, end)))


protocol_group.add_command(get_bonding_req)


@command()
@rpc_endpoint_option
@argument("start", type=int, nargs=1)
@argument("end", type=int, nargs=1)
def get_unbonding_req(rpc_endpoint: Optional[str], start: int, end: int) -> None:
    """
    Get queued unbonding information between start and end ids.
    """
    from aut.utils import web3_from_endpoint_arg
    from autonity import Autonity

    aut = Autonity(web3_from_endpoint_arg(None, rpc_endpoint))
    print(_show_json(aut.get_unbonding_req(start, end)))


protocol_group.add_command(get_unbonding_req)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("base-fee-str", metavar="base-fee", nargs=1)
def set_minimum_base_fee(
    rpc_endpoint: Optional[str],
    keyfile: Optional[str],
    from_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    base_fee_str: str,
) -> None:
    """
    Set the minimum gas price. Restricted to the operator account.
    See `setMinimumBaseFee` on the Autonity contract.
    """
    from aut.utils import (
        autonity_from_endpoint_arg,
        from_address_from_argument,
        create_contract_tx_from_args,
        parse_wei_representation,
        to_json,
    )

    base_fee = parse_wei_representation(base_fee_str)
    from_addr = from_address_from_argument(from_str, keyfile)
    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.set_minimum_base_fee(base_fee),
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


protocol_group.add_command(set_minimum_base_fee)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("committee-size", type=int, nargs=1)
def set_committee_size(
    rpc_endpoint: Optional[str],
    keyfile: Optional[str],
    from_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    committee_size: int,
) -> None:
    """
    Set the maximum size of the consensus committee. Restricted to the
    Operator account.  See `setCommitteeSize` on Autonity contract.
    """
    from aut.utils import (
        autonity_from_endpoint_arg,
        from_address_from_argument,
        create_contract_tx_from_args,
        to_json,
    )

    from_addr = from_address_from_argument(from_str, keyfile)
    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.set_committee_size(committee_size),
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


protocol_group.add_command(set_committee_size)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("unbonding-period", type=int, nargs=1)
def set_unbonding_period(
    rpc_endpoint: Optional[str],
    keyfile: Optional[str],
    from_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    unbonding_period: int,
) -> None:
    """
    Set the unbonding period. Restricted to the Operator account.  See
    `setUnbondingPeriod` on Autonity contract.
    """
    from aut.utils import (
        autonity_from_endpoint_arg,
        from_address_from_argument,
        create_contract_tx_from_args,
        to_json,
    )

    from_addr = from_address_from_argument(from_str, keyfile)
    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.set_unbonding_period(unbonding_period),
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


protocol_group.add_command(set_unbonding_period)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("epoch-period", type=int, nargs=1)
def set_epoch_period(
    rpc_endpoint: Optional[str],
    keyfile: Optional[str],
    from_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    epoch_period: int,
) -> None:
    """
    Set the epoch period. Restricted to the Operator account.  See
    `setEpochPeriod` on Autonity contract.
    """
    from aut.utils import (
        autonity_from_endpoint_arg,
        from_address_from_argument,
        create_contract_tx_from_args,
        to_json,
    )

    from_addr = from_address_from_argument(from_str, keyfile)
    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.set_epoch_period(epoch_period),
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


protocol_group.add_command(set_epoch_period)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("operator-address-str", metavar="OPERATOR-ADDRESS", nargs=1)
def set_operator_account(
    rpc_endpoint: Optional[str],
    keyfile: Optional[str],
    from_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    operator_address_str: str,
) -> None:
    """
    Set the Operator account. Restricted to the Operator account.  See
    `setOperatorAccount` on Autonity contract.
    """
    from aut.utils import (
        autonity_from_endpoint_arg,
        from_address_from_argument,
        create_contract_tx_from_args,
        to_json,
    )

    from eth_utils import to_checksum_address

    operator_address = to_checksum_address(operator_address_str)
    from_addr = from_address_from_argument(from_str, keyfile)
    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.set_operator_account(operator_address),
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


protocol_group.add_command(set_operator_account)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("treasury-address-str", metavar="treasury-address", nargs=1)
def set_treasury_account(
    rpc_endpoint: Optional[str],
    keyfile: Optional[str],
    from_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    treasury_address_str: str,
) -> None:
    """
    Set the global treasury account. Restricted to the Operator
    account.  See `setTreasuryAccount` on Autonity contract.
    """
    from aut.utils import (
        autonity_from_endpoint_arg,
        from_address_from_argument,
        create_contract_tx_from_args,
        to_json,
    )

    from eth_utils import to_checksum_address

    treasury_address = to_checksum_address(treasury_address_str)
    from_addr = from_address_from_argument(from_str, keyfile)
    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.set_treasury_account(treasury_address),
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


protocol_group.add_command(set_treasury_account)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("treasury-fee-str", metavar="TREASURY-FEE", nargs=1)
def set_treasury_fee(
    rpc_endpoint: Optional[str],
    keyfile: Optional[str],
    from_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    treasury_fee_str: str,
) -> None:
    """
    Set the treasury fee. Restricted to the Operator account.  See
    `setTreasuryFee` on Autonity contract.
    """
    from aut.utils import (
        autonity_from_endpoint_arg,
        from_address_from_argument,
        create_contract_tx_from_args,
        parse_wei_representation,
        to_json,
    )

    treasury_fee = parse_wei_representation(treasury_fee_str)
    from_addr = from_address_from_argument(from_str, keyfile)
    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.set_treasury_fee(treasury_fee),
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


protocol_group.add_command(set_treasury_fee)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("amount-str", metavar="AMOUNT", nargs=1)
@argument("recipient-str", metavar="RECIPIENT", required=False)
def mint(
    rpc_endpoint: Optional[str],
    keyfile: Optional[str],
    from_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    amount_str: str,
    recipient_str: Optional[str],
) -> None:
    """
    Mint new stake token (NTN) and add it to the recipient balance. If
    recipient is not specified, the caller's address is used.
    Restricted to the Operator account.  See `mint` on Autonity
    contract.
    """
    from aut.utils import (
        autonity_from_endpoint_arg,
        from_address_from_argument,
        create_contract_tx_from_args,
        parse_newton_value_representation,
        to_json,
    )

    from eth_utils import to_checksum_address

    token_units = parse_newton_value_representation(amount_str)
    from_addr = from_address_from_argument(from_str, keyfile)
    recipient = to_checksum_address(recipient_str) if recipient_str else from_addr

    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.mint(recipient, token_units),
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


protocol_group.add_command(mint)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("amount-str", metavar="AMOUNT")
@argument("account-str", metavar="ACCOUNT", required=False)
def burn(
    rpc_endpoint: Optional[str],
    keyfile: Optional[str],
    from_str: Optional[str],
    gas: Optional[str],
    gas_price: Optional[str],
    max_priority_fee_per_gas: Optional[str],
    max_fee_per_gas: Optional[str],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    amount_str: str,
    account_str: Optional[str],
) -> None:
    """
    Burn the specified amount of NTN stake token from an account.  If
    account is not specified, the caller's address is used. Restricted
    to the Operator account.  This won't burn associated Liquid
    tokens.  See `burn` on Autonity contract.
    """
    from aut.utils import (
        autonity_from_endpoint_arg,
        from_address_from_argument,
        create_contract_tx_from_args,
        parse_newton_value_representation,
        to_json,
    )

    from eth_utils import to_checksum_address

    token_units = parse_newton_value_representation(amount_str)
    from_addr = from_address_from_argument(from_str, keyfile)
    account = to_checksum_address(account_str) if account_str else from_addr
    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.burn(account, token_units),
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


protocol_group.add_command(burn)
