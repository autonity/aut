"""
The `gov` command group.
"""

from typing import Optional

from autonity import Autonity
from click import argument, command, group
from eth_typing import ChecksumAddress
from web3 import Web3
from web3.types import Wei

from ..options import (
    config_option,
    from_option,
    keyfile_option,
    rpc_endpoint_option,
    tx_aux_options,
)
from ..utils import (
    create_contract_tx_from_args,
    from_address_from_argument,
    to_json,
)
from ..param_types import ChecksumAddressType, TokenValueType


@group(name="governance")
def governance_group() -> None:
    """Commands that can only be called by the governance operator account."""


@command()
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("gas_value", metavar="gas", type=TokenValueType())
def set_max_bond_applied_gas(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    gas_value: Wei,
) -> None:
    """Set the maximum bond applied gas.

    Restricted to the operator account.
    See `setMaxBondAppliedGas` on the Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    aut = Autonity(w3)

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
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("gas_value", metavar="gas", type=TokenValueType())
def set_max_unbond_applied_gas(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    gas_value: Wei,
) -> None:
    """Set the maximum unbond applied gas.

    Restricted to the operator account.
    See `setMaxBondAppliedGas` on the Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    aut = Autonity(w3)

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
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("gas_value", metavar="gas", type=TokenValueType())
def set_max_unbond_released_gas(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    gas_value: Wei,
) -> None:
    """Set the maximum unbond released gas.

    Restricted to the operator account.
    See `setMaxBondAppliedGas` on the Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    aut = Autonity(w3)

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
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("gas_value", metavar="gas", type=TokenValueType())
def set_max_rewards_distribution_gas(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    gas_value: Wei,
) -> None:
    """Set the maximum rewards distribution gas.

    Restricted to the operator account.
    See `setMaxBondAppliedGas` on the Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    aut = Autonity(w3)

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
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("gas_value", metavar="gas", type=TokenValueType())
def set_staking_gas_price(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    gas_value: Wei,
) -> None:
    """Set the gas price for notification on staking operation.

    Restricted to the operator account.
    See `setStakingGasPrice` on the Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    aut = Autonity(w3)

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
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("base-fee", type=TokenValueType())
def set_minimum_base_fee(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    base_fee: Wei,
) -> None:
    """Set the minimum gas price.

    Restricted to the operator account.
    See `setMinimumBaseFee` on the Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    aut = Autonity(w3)

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
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("committee-size", type=int)
def set_committee_size(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    committee_size: int,
) -> None:
    """Set the maximum size of the consensus committee.

    Restricted to the Operator account. See `setCommitteeSize` on Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    aut = Autonity(w3)

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
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("unbonding-period", type=int)
def set_unbonding_period(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    unbonding_period: int,
) -> None:
    """Set the unbonding period.

    Restricted to the Operator account. See `setUnbondingPeriod` on Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    aut = Autonity(w3)

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
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("epoch-period", type=int)
def set_epoch_period(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    epoch_period: int,
) -> None:
    """Set the epoch period.

    Restricted to the Operator account. See `setEpochPeriod` on Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    aut = Autonity(w3)

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
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("operator-address", type=ChecksumAddressType())
def set_operator_account(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    operator_address: ChecksumAddress,
) -> None:
    """Set the Operator account.

    Restricted to the Operator account. See `setOperatorAccount` on Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    aut = Autonity(w3)

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
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("treasury-address", type=ChecksumAddressType())
def set_treasury_account(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    treasury_address: ChecksumAddress,
) -> None:
    """Set the global treasury account.

    Restricted to the Operator account. See `setTreasuryAccount` on Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    aut = Autonity(w3)

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
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("treasury-fee", type=TokenValueType())
def set_treasury_fee(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    treasury_fee: Wei,
) -> None:
    """Set the treasury fee.

    Restricted to the Operator account. See `setTreasuryFee` on Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    aut = Autonity(w3)

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
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("contract-address", type=ChecksumAddressType())
def set_accountability_contract(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    contract_address: ChecksumAddress,
) -> None:
    """Set the Accountability Contract address.

    Restricted to the Operator account.
    See `setAccountabilityContract` on Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    aut = Autonity(w3)

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
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("contract-address", type=ChecksumAddressType())
def set_oracle_contract(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    contract_address: ChecksumAddress,
) -> None:
    """Set the Oracle Contract address.

    Restricted to the Operator account. See `setOracleContract` on Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    aut = Autonity(w3)

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
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("contract-address", type=ChecksumAddressType())
def set_acu_contract(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    contract_address: ChecksumAddress,
) -> None:
    """Set the ACU Contract address.

    Restricted to the Operator account. See `setAcuContract` on Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    aut = Autonity(w3)

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
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("contract-address", type=ChecksumAddressType())
def set_supply_control_contract(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    contract_address: ChecksumAddress,
) -> None:
    """Set the Supply Control Contract address.

    Restricted to the Operator account.
    See `setSupplyControlContract` on Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    aut = Autonity(w3)

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
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("contract-address", type=ChecksumAddressType())
def set_stabilization_contract(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    contract_address: ChecksumAddress,
) -> None:
    """Set the Supply Control Contract address.

    Restricted to the Operator account.
    See `setSupplyControlContract` on Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    aut = Autonity(w3)

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
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("contract-address-str", type=ChecksumAddressType())
def set_inflation_controller_contract(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    contract_address: ChecksumAddress,
) -> None:
    """Set the inflation controller contract address.

    Restricted to the Operator account.
    See `setInflationControllerContract` on Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    aut = Autonity(w3)

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
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("contract-address", type=ChecksumAddressType())
def set_upgrade_manager_contract(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    contract_address: ChecksumAddress,
) -> None:
    """Set the upgrade manager contract address.

    Restricted to the Operator account.
    See `setUpgradeManagerContract` on Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    aut = Autonity(w3)

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
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("contract-address", type=ChecksumAddressType())
def set_non_stakable_vesting_contract(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    contract_address: ChecksumAddress,
) -> None:
    """Set the non stakable vesting contract address.

    Restricted to the Operator account.
    See `setNonStakableVestingContract` on Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    aut = Autonity(w3)

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
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("amount", type=TokenValueType())
@argument("recipient", type=ChecksumAddressType(), required=False)
def mint(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    amount: Wei,
    recipient: Optional[ChecksumAddress],
) -> None:
    """Mint new stake token (NTN) and add it to the recipient balance.

    If recipient is not specified, the caller's address is used.
    Restricted to the Operator account. See `mint` on Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    recipient = recipient if recipient else from_addr

    aut = Autonity(w3)

    tx = create_contract_tx_from_args(
        function=aut.mint(recipient, amount),
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
@config_option
@rpc_endpoint_option
@keyfile_option()
@from_option
@tx_aux_options
@argument("amount", type=ChecksumAddressType())
@argument("account", type=ChecksumAddressType(), required=False)
def burn(
    w3: Web3,
    keyfile: Optional[str],
    from_: Optional[ChecksumAddress],
    gas: Optional[int],
    gas_price: Optional[Wei],
    max_priority_fee_per_gas: Optional[Wei],
    max_fee_per_gas: Optional[Wei],
    fee_factor: Optional[float],
    nonce: Optional[int],
    chain_id: Optional[int],
    amount: Wei,
    account: Optional[ChecksumAddress],
) -> None:
    """Burn the specified amount of NTN stake token from an account.

    If account is not specified, the caller's address is used.
    Restricted to the Operator account. This won't burn associated Liquid
    tokens. See `burn` on Autonity contract.
    """

    from_addr = from_address_from_argument(from_, keyfile)
    account = account if account else from_addr
    aut = Autonity(w3)

    tx = create_contract_tx_from_args(
        function=aut.burn(account, amount),
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
