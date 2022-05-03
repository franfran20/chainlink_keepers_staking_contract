# stake fucntion
def stakeToken(stake_contract, token_address, amount, acct):
    tx = stake_contract.stake(token_address, amount, {"from": acct})
    tx.wait(1)


# unstake func
def unStakeToken(stake_contract, token_address, amount, acct):
    tx = stake_contract.unStake(token_address, amount, {"from": acct})
    tx.wait(1)


# approve func
def approve(token_contract, spender, amount, acct):
    tx = token_contract.approve(spender, amount, {"from": acct})
    tx.wait(1)
