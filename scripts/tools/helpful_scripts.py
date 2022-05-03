from brownie import accounts, network, KeeperMock
from web3 import Web3

# deployment variables
INTERVAL = 600
TOTAL_SUPPLY = Web3.toWei(1000000, "ether")
DISTRIBUTE_AMOUNT = Web3.toWei(10000, "ether")

# Deployments and testig
STAKE_AMOUNT = Web3.toWei(10000, "ether")

# get account based on a network
def get_account(index=None, id=None):
    if network.show_active() in ["development"]:
        return accounts[0]
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)


# distribute tokens to other accounts on deployment for local testing
def distribute_tokens(token_contract):
    if network.show_active() == "development":
        tx_1 = token_contract.transfer(
            accounts[1].address, DISTRIBUTE_AMOUNT, {"from": accounts[0]}
        )
        tx_1.wait(1)
        tx_2 = token_contract.transfer(
            accounts[2].address, DISTRIBUTE_AMOUNT, {"from": accounts[0]}
        )
        tx_2.wait(1)


# mock the chainlink keeper
def deploy_keeper_mock(stake_contract_address, account):
    keeper_mock = KeeperMock.deploy(stake_contract_address, {"from": account})
    return keeper_mock
