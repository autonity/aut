"""
The `gov` command group.
"""

from typing import Optional

from click import argument, command, group
from eth_utils import to_checksum_address

from aut.options import from_option, keyfile_option, rpc_endpoint_option, tx_aux_options
from aut.utils import (
    autonity_from_endpoint_arg,
    create_contract_tx_from_args,
    from_address_from_argument,
    parse_newton_value_representation,
    parse_wei_representation,
    to_json,
)


@group(name="governance")
def governance_group() -> None:
    """
    Commands that can only be called by the governance operator account.
    """


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("gas_value_str", metavar="gas", nargs=1)
def set_max_bond_applied_gas(
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
    gas_value_str: str,
) -> None:
    """
    Set the maximum bond applied gas. Restricted to the operator account.
    See `setMaxBondAppliedGas` on the Autonity contract.
    """

    gas_value = parse_wei_representation(gas_value_str)
    from_addr = from_address_from_argument(from_str, keyfile)
    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.set_max_bond_applied_gas(gas_value),
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


governance_group.add_command(set_max_bond_applied_gas)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("gas_value_str", metavar="gas", nargs=1)
def set_max_unbond_applied_gas(
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
    gas_value_str: str,
) -> None:
    """
    Set the maximum unbond applied gas. Restricted to the operator account.
    See `setMaxBondAppliedGas` on the Autonity contract.
    """

    gas_value = parse_wei_representation(gas_value_str)
    from_addr = from_address_from_argument(from_str, keyfile)
    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.set_max_unbond_applied_gas(gas_value),
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


governance_group.add_command(set_max_unbond_applied_gas)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("gas_value_str", metavar="gas", nargs=1)
def set_max_unbond_released_gas(
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
    gas_value_str: str,
) -> None:
    """
    Set the maximum unbond released gas. Restricted to the operator account.
    See `setMaxBondAppliedGas` on the Autonity contract.
    """

    gas_value = parse_wei_representation(gas_value_str)
    from_addr = from_address_from_argument(from_str, keyfile)
    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.set_max_unbond_released_gas(gas_value),
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


governance_group.add_command(set_max_unbond_released_gas)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("gas_value_str", metavar="gas", nargs=1)
def set_max_rewards_distribution_gas(
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
    gas_value_str: str,
) -> None:
    """
    Set the maximum rewards distribution gas. Restricted to the operator account.
    See `setMaxBondAppliedGas` on the Autonity contract.
    """

    gas_value = parse_wei_representation(gas_value_str)
    from_addr = from_address_from_argument(from_str, keyfile)
    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.set_max_rewards_distribution_gas(gas_value),
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


governance_group.add_command(set_max_rewards_distribution_gas)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("gas_value_str", metavar="gas", nargs=1)
def set_staking_gas_price(
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
    gas_value_str: str,
) -> None:
    """
    Set the gas price for notification on staking operation. Restricted to the
    operator account. See `setStakingGasPrice` on the Autonity contract.
    """

    gas_value = parse_wei_representation(gas_value_str)
    from_addr = from_address_from_argument(from_str, keyfile)
    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.set_staking_gas_price(gas_value),
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


governance_group.add_command(set_staking_gas_price)


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


governance_group.add_command(set_minimum_base_fee)


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


governance_group.add_command(set_committee_size)


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


governance_group.add_command(set_unbonding_period)


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


governance_group.add_command(set_epoch_period)


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


governance_group.add_command(set_operator_account)


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


governance_group.add_command(set_treasury_account)


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


governance_group.add_command(set_treasury_fee)


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


governance_group.add_command(set_accountability_contract)


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


governance_group.add_command(set_oracle_contract)


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


governance_group.add_command(set_acu_contract)


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


governance_group.add_command(set_supply_control_contract)


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


governance_group.add_command(set_stabilization_contract)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("contract-address-str", metavar="CONTRACT-ADDRESS", nargs=1)
def set_inflation_controller_contract(
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
    Set the inflation controller contract address. Restricted to the Operator
    account. See `setInflationControllerContract` on Autonity contract.
    """

    contract_address = to_checksum_address(contract_address_str)
    from_addr = from_address_from_argument(from_str, keyfile)
    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.set_inflation_controller_contract(contract_address),
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


governance_group.add_command(set_inflation_controller_contract)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("contract-address-str", metavar="CONTRACT-ADDRESS", nargs=1)
def set_upgrade_manager_contract(
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
    Set the upgrade manager contract address. Restricted to the Operator account.
    See `setUpgradeManagerContract` on Autonity contract.
    """

    contract_address = to_checksum_address(contract_address_str)
    from_addr = from_address_from_argument(from_str, keyfile)
    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.set_upgrade_manager_contract(contract_address),
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


governance_group.add_command(set_upgrade_manager_contract)


@command()
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("contract-address-str", metavar="CONTRACT-ADDRESS", nargs=1)
def set_non_stakable_vesting_contract(
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
    Set the non stakable vesting contract address. Restricted to the Operator
    account. See `setNonStakableVestingContract` on Autonity contract.
    """

    contract_address = to_checksum_address(contract_address_str)
    from_addr = from_address_from_argument(from_str, keyfile)
    aut = autonity_from_endpoint_arg(rpc_endpoint)

    tx = create_contract_tx_from_args(
        function=aut.set_non_stakable_vesting_contract(contract_address),
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


governance_group.add_command(set_non_stakable_vesting_contract)


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


governance_group.add_command(mint)


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


governance_group.add_command(burn)
