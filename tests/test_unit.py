import pytest
from brownie import accounts, network, exceptions
from web3 import Web3
from scripts.tools.helpful_scripts import (
    STAKE_AMOUNT,
    deploy_keeper_mock,
    get_account,
)
from scripts.deploy import deploy
from scripts.tools.helpful_test_functions import (
    approve,
    stakeToken,
    unStakeToken,
)


def test_is_token_supported():
    if network.show_active() != "development":
        pytest.skip("Only for local testing")
    (staking_contract, stake_token, supported_tokens) = deploy()
    tx = staking_contract.isTokenSupported(stake_token.address)
    bool_val = tx.return_value
    assert bool_val == True


def test_user_can_stake_supported_tokens():
    account = get_account()
    (staking_contract, stake_token, supported_tokens) = deploy()

    approve(stake_token, staking_contract.address, STAKE_AMOUNT, account)
    approve(stake_token, staking_contract.address, STAKE_AMOUNT, accounts[1])
    approve(stake_token, staking_contract.address, STAKE_AMOUNT, accounts[2])

    stakeToken(staking_contract, stake_token.address, STAKE_AMOUNT, accounts[1])
    stakeToken(staking_contract, stake_token.address, STAKE_AMOUNT, accounts[2])

    assert (
        staking_contract.normalBalances(accounts[1].address, stake_token.address)
        == STAKE_AMOUNT
    )
    assert (
        staking_contract.normalBalances(accounts[2].address, stake_token.address)
        == STAKE_AMOUNT
    )


def test_can_unstake_supported_tokens():
    account = get_account()
    (staking_contract, stake_token, supported_tokens) = deploy()

    approve(stake_token, staking_contract.address, STAKE_AMOUNT, account)
    approve(stake_token, staking_contract.address, STAKE_AMOUNT, accounts[1])
    approve(stake_token, staking_contract.address, STAKE_AMOUNT, accounts[2])

    stakeToken(staking_contract, stake_token.address, STAKE_AMOUNT, accounts[1])
    stakeToken(staking_contract, stake_token.address, STAKE_AMOUNT, accounts[2])

    unStakeToken(staking_contract, stake_token.address, STAKE_AMOUNT, accounts[1])
    unStakeToken(staking_contract, stake_token.address, STAKE_AMOUNT, accounts[2])

    assert (
        staking_contract.normalBalances(accounts[1].address, stake_token.address) == 0
    )
    assert (
        staking_contract.normalBalances(accounts[2].address, stake_token.address) == 0
    )


def test_only_contract_can_mint_extra_tokens():
    account = get_account()
    (staking_contract, stake_token, supported_tokens) = deploy()
    # we've transferred ownership already!!
    with pytest.raises(exceptions.VirtualMachineError):
        stake_token.mint(account.address, STAKE_AMOUNT, {"from": account})


def test_issue_rewards():
    account = get_account()
    (
        staking_contract,
        stake_token,
        supported_tokens,
    ) = deploy()

    approve(stake_token, staking_contract.address, STAKE_AMOUNT, accounts[1])
    approve(stake_token, staking_contract.address, STAKE_AMOUNT, accounts[2])

    stakeToken(staking_contract, stake_token.address, STAKE_AMOUNT, accounts[1])
    stakeToken(staking_contract, stake_token.address, STAKE_AMOUNT, accounts[2])

    # mock keeper
    # remember to change the issuereward func visibility to public before testing!!!
    keeper_mock = deploy_keeper_mock(staking_contract.address, account)
    keeper_mock.mockPerformUpkeep({"from": account})

    # received amount
    received_amount = Web3.toWei(5000, "ether")
    assert stake_token.balanceOf(accounts[1].address) == received_amount
    assert stake_token.balanceOf(accounts[2].address) == received_amount
