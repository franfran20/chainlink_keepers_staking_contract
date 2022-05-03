//SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "../StakingContract.sol";

contract KeeperMock{
    StakingContract public stakingContract;
    bytes public fakebytes;
    constructor(StakingContract _stakingContract){
        stakingContract = StakingContract(_stakingContract);
    }

    function mockPerformUpkeep() public {
        stakingContract.issueRewards();
    }
}