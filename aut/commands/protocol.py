"""
The `autonity` command group.
"""

from typing import Any, Optional, Sequence

from autonity import AUTONITY_CONTRACT_ADDRESS, Autonity
from click import argument, command, echo, group
from eth_utils import to_checksum_address

from aut.options import (from_option, keyfile_option, rpc_endpoint_option,
                         tx_aux_options)
from aut.utils import (autonity_from_endpoint_arg,
                       create_contract_tx_from_args,
                       from_address_from_argument,
                       parse_newton_value_representation,
                       parse_wei_representation, to_json)

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
    return to_json(value, pretty=True)


@command()
@rpc_endpoint_option
def commission_rate_precision(rpc_endpoint: Optional[str]) -> None:
    """
    Precision of validator commission rate values
    """

    print(autonity_from_endpoint_arg(rpc_endpoint).commission_rate_precision())


protocol_group.add_command(commission_rate_precision)


@command()
@rpc_endpoint_option
def config(rpc_endpoint: Optional[str]) -> None:
    """
    Print the Autonity contract config
    """

    print(_show_json(autonity_from_endpoint_arg(rpc_endpoint).config()))


protocol_group.add_command(config)


@command()
@rpc_endpoint_option
def epoch_id(rpc_endpoint: Optional[str]) -> None:
    """
    ID of current epoch
    """

    print(autonity_from_endpoint_arg(rpc_endpoint).epoch_id())


protocol_group.add_command(epoch_id)


@command()
@rpc_endpoint_option
def last_epoch_block(rpc_endpoint: Optional[str]) -> None:
    """
    Block number of the last epoch
    """

    print(autonity_from_endpoint_arg(rpc_endpoint).last_epoch_block())


protocol_group.add_command(last_epoch_block)


@command()
@rpc_endpoint_option
def epoch_total_bonded_stake(rpc_endpoint: Optional[str]) -> None:
    """
    Total stake bonded this epoch
    """

    print(autonity_from_endpoint_arg(rpc_endpoint).epoch_total_bonded_stake())


protocol_group.add_command(epoch_total_bonded_stake)


@command()
@rpc_endpoint_option
def total_redistributed(rpc_endpoint: Optional[str]) -> None:
    """
    Total fees redistributed
    """

    print(autonity_from_endpoint_arg(rpc_endpoint).total_redistributed())


protocol_group.add_command(total_redistributed)


@command()
@rpc_endpoint_option
def epoch_reward(rpc_endpoint: Optional[str]) -> None:
    """
    Reward for this epoch
    """

    print(autonity_from_endpoint_arg(rpc_endpoint).epoch_reward())


protocol_group.add_command(epoch_reward)


@command()
@rpc_endpoint_option
def deployer(rpc_endpoint: Optional[str]) -> None:
    """
    Contract deployer
    """

    print(autonity_from_endpoint_arg(rpc_endpoint).deployer())


protocol_group.add_command(deployer)


@command()
@rpc_endpoint_option
def get_epoch_period(rpc_endpoint: Optional[str]) -> None:
    """Epoch period in blocks"""

    print(autonity_from_endpoint_arg(rpc_endpoint).get_epoch_period())


protocol_group.add_command(get_epoch_period)


@command()
@rpc_endpoint_option
def get_block_period(rpc_endpoint: Optional[str]) -> None:
    """Block period in seconds"""

    print(autonity_from_endpoint_arg(rpc_endpoint).get_block_period())


protocol_group.add_command(get_block_period)


@command()
@rpc_endpoint_option
def get_unbonding_period(rpc_endpoint: Optional[str]) -> None:
    """Unbonding period in blocks"""

    print(autonity_from_endpoint_arg(rpc_endpoint).get_unbonding_period())


protocol_group.add_command(get_unbonding_period)


@command()
@rpc_endpoint_option
def get_last_epoch_block(rpc_endpoint: Optional[str]) -> None:
    """
    Block of last epoch
    """

    print(autonity_from_endpoint_arg(rpc_endpoint).get_last_epoch_block())


protocol_group.add_command(get_last_epoch_block)


@command()
@rpc_endpoint_option
def get_version(rpc_endpoint: Optional[str]) -> None:
    """Contract version"""

    print(autonity_from_endpoint_arg(rpc_endpoint).get_version())


protocol_group.add_command(get_version)


@command()
@rpc_endpoint_option
def get_committee(rpc_endpoint: Optional[str]) -> None:
    """
    Get current committee"
    """

    print(_show_json(autonity_from_endpoint_arg(rpc_endpoint).get_committee()))


protocol_group.add_command(get_committee)


@command()
@rpc_endpoint_option
def get_validators(rpc_endpoint: Optional[str]) -> None:
    """Get current validators"""

    print(_show_sequence(autonity_from_endpoint_arg(rpc_endpoint).get_validators()))


protocol_group.add_command(get_validators)


@command()
@rpc_endpoint_option
def get_treasury_account(rpc_endpoint: Optional[str]) -> None:
    """Treasury account address"""

    print(autonity_from_endpoint_arg(rpc_endpoint).get_treasury_account())


protocol_group.add_command(get_treasury_account)


@command()
@rpc_endpoint_option
def get_treasury_fee(rpc_endpoint: Optional[str]) -> None:
    """Treasury fee"""

    print(autonity_from_endpoint_arg(rpc_endpoint).get_treasury_fee())


protocol_group.add_command(get_treasury_fee)


@command()
@rpc_endpoint_option
def get_max_committee_size(rpc_endpoint: Optional[str]) -> None:
    """Maximum committee size"""

    print(autonity_from_endpoint_arg(rpc_endpoint).get_max_committee_size())


protocol_group.add_command(get_max_committee_size)


@command()
@rpc_endpoint_option
def get_committee_enodes(rpc_endpoint: Optional[str]) -> None:
    """Enodes in current committee"""

    print(autonity_from_endpoint_arg(rpc_endpoint).get_committee_enodes())


protocol_group.add_command(get_committee_enodes)


@command()
@rpc_endpoint_option
def get_minimum_base_fee(rpc_endpoint: Optional[str]) -> None:
    """Minimum base fee"""

    print(autonity_from_endpoint_arg(rpc_endpoint).get_minimum_base_fee())


protocol_group.add_command(get_minimum_base_fee)


@command()
@rpc_endpoint_option
def get_operator(rpc_endpoint: Optional[str]) -> None:
    """Contract operator"""

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

    aut = Autonity(web3_from_endpoint_arg(None, rpc_endpoint))
    print(aut.get_proposer(height, round_))


protocol_group.add_command(get_proposer)


@command()
@rpc_endpoint_option
@argument("block", type=int, nargs=1)
def get_epoch_from_block(rpc_endpoint: Optional[str], block: int) -> None:
    """Get the epoch of the given block"""

    aut = Autonity(web3_from_endpoint_arg(None, rpc_endpoint))
    print(aut.get_epoch_from_block(block))


protocol_group.add_command(get_epoch_from_block)


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
@argument("contract-address-str", metavar="CONTRACT-ADDRESS", nargs=1)
def set_accountability_contract(
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
    contract_address_str: str,
) -> None:
    """
    Set the Accountability Contract address. Restricted to the Operator account.  See
    `setAccountabilityContract` on Autonity contract.
    """

    contract_address = to_checksum_address(contract_address_str)
    from_addr = from_address_from_argument(from_str, keyfile)
    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.set_accountability_contract(contract_address),
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


protocol_group.add_command(set_accountability_contract)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("contract-address-str", metavar="CONTRACT-ADDRESS", nargs=1)
def set_oracle_contract(
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
    contract_address_str: str,
) -> None:
    """
    Set the Oracle Contract address. Restricted to the Operator account.  See
    `setOracleContract` on Autonity contract.
    """

    contract_address = to_checksum_address(contract_address_str)
    from_addr = from_address_from_argument(from_str, keyfile)
    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.set_oracle_contract(contract_address),
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


protocol_group.add_command(set_oracle_contract)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("contract-address-str", metavar="CONTRACT-ADDRESS", nargs=1)
def set_acu_contract(
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
    contract_address_str: str,
) -> None:
    """
    Set the ACU Contract address. Restricted to the Operator account.  See
    `setAcuContract` on Autonity contract.
    """

    contract_address = to_checksum_address(contract_address_str)
    from_addr = from_address_from_argument(from_str, keyfile)
    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.set_acu_contract(contract_address),
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


protocol_group.add_command(set_acu_contract)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("contract-address-str", metavar="CONTRACT-ADDRESS", nargs=1)
def set_supply_control_contract(
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
    contract_address_str: str,
) -> None:
    """
    Set the Supply Control Contract address. Restricted to the Operator account.  See
    `setSupplyControlContract` on Autonity contract.
    """

    contract_address = to_checksum_address(contract_address_str)
    from_addr = from_address_from_argument(from_str, keyfile)
    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.set_supply_control_contract(contract_address),
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


protocol_group.add_command(set_supply_control_contract)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("contract-address-str", metavar="CONTRACT-ADDRESS", nargs=1)
def set_stabilization_contract(
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
    contract_address_str: str,
) -> None:
    """
    Set the Supply Control Contract address. Restricted to the Operator account.  See
    `setSupplyControlContract` on Autonity contract.
    """

    contract_address = to_checksum_address(contract_address_str)
    from_addr = from_address_from_argument(from_str, keyfile)
    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.set_stabilization_contract(contract_address),
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


protocol_group.add_command(set_stabilization_contract)


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


@command()
def contract_address() -> None:
    """
    Print the default Autonity contract address.
    """

    echo(AUTONITY_CONTRACT_ADDRESS, nl=False)


protocol_group.add_command(contract_address)
