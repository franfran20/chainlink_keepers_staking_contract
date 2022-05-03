import time
from brownie import StakingContract, StakeToken, network
from requests import get
from scripts.tools.helpful_test_functions import (
    approve,
    stakeToken,
    unStakeToken,
)
from scripts.tools.helpful_scripts import (
    INTERVAL,
    STAKE_AMOUNT,
    distribute_tokens,
    get_account,
)


def deploy():
    if network.show_active() == "development":
        account = get_account()
    else:
        # using my id to deploy, use yours or add your priv key to .env
        # i use this wallet only for TESTING!!. I advise you do the same.
        account = get_account(id="Your own id!")

    print("Deploying stake token...")
    stake_token = StakeToken.deploy("StakeToken", "STK", {"from": account})
    supported_tokens = [stake_token.address]

    print("Deploying staking contract...")
    staking_contract = StakingContract.deploy(
        supported_tokens,
        stake_token.address,
        INTERVAL,
        {"from": account},
        # publish_source=True,
    )
    # distribute stake tokens
    if network.show_active() == "development":
        print("Distributing stake token...")
        distribute_tokens(stake_token)

    print("Transferring stake token ownership to contract..")
    stake_token.transferOwnership(staking_contract.address, {"from": account})

    print("all done!")
    return (
        staking_contract,
        stake_token,
        supported_tokens,
    )


def stake():
    account = get_account(id="francis-test")
    approve(StakeToken[-1], StakingContract[-1].address, STAKE_AMOUNT, account)
    stakeToken(StakingContract[-1], StakeToken[-1].address, STAKE_AMOUNT, account)

    print(f"{StakeToken[-1].balanceOf(account.address)}")


def unstake():
    account = get_account(id="francis-test")
    unStakeToken(StakingContract[-1], StakeToken[-1].address, STAKE_AMOUNT, account)


def check_balance():
    account = get_account(id="francis-test")
    print(f"{StakeToken[-1].balanceOf(account.address)}")


def main():
    deploy()
    stake()
    check_balance()
    # wait for keepers
    time.sleep(610)
    check_balance()
