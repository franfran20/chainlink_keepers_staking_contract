//SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@chainlink/contracts/src/v0.8/KeeperCompatible.sol";
import "./StakeToken.sol";


//the contract was initially made to add extra support for different tokens
//but doing that and keeping it decentralized means that a DAO has to govern this
//will probably modify this repo and add that feature in the future. 

//For now enjoy the powerful feature of chainlink keepers!! :)

contract StakingContract is ReentrancyGuard, KeeperCompatibleInterface {
    address[] supportedTokens;
    address[] depositors;
    address public PoolAddress;
    mapping(address => mapping(address => uint256)) public normalBalances;
    StakeToken public stakeToken;

    //chainlink keepers
    uint256 public immutable interval;
    uint256 public lastTimeStamp;

    constructor(
        address[] memory _supportedTokens,
        address _StakeTokenAddress,
        uint256 _interval
    ) {
        supportedTokens = _supportedTokens;
        stakeToken = StakeToken(_StakeTokenAddress);
        interval = _interval;
        lastTimeStamp = block.timestamp;  
    }

    //allow users stake
    function stake(
        address _token,
        uint256 _amount
    ) public {
        require(_token != address(0), "Invalid Token Address");
        require(_amount > 0, "Invalid stake amount");
        require(isTokenSupported(_token), "Token isnt supported by us");

        IERC20(_token).transferFrom(
            msg.sender,
            address(this),
            _amount
        );
        normalBalances[msg.sender][_token] += _amount; 
        depositors.push(msg.sender);
    
    }    

    //allows users to unstake
    function unStake(
        address _token,
        uint256 _amount
    ) public nonReentrant{

        require(
            _amount <= normalBalances[msg.sender][_token],
            "Insuficient Balance"
        );
        normalBalances[msg.sender][_token] -= _amount;
        IERC20(_token).transfer(msg.sender, _amount);

    }

    //chainlink node checking how often our code should be checked up on!
    //thats awesome, chainlink cares!!!
    function checkUpkeep(
        bytes calldata /* checkData */
    )
        external
        view
        override
        returns (
            bool upkeepNeeded,
            bytes memory /* performData */
        )
    {
        upkeepNeeded = (block.timestamp - lastTimeStamp) > interval;
    }

    //chainlink calling this function for us in A DECENTRALIZED manner! Awesome!
    function performUpkeep(bytes calldata) external override {
        if ((block.timestamp - lastTimeStamp) > interval) {
            lastTimeStamp = block.timestamp;
            issueRewards();
        }
    }

    //change to public for local testing
    function issueRewards() private {
        //transfer ownership to this contract
        for (uint256 user = 0; user < depositors.length; user++) {
            if (
                normalBalances[depositors[user]][address(stakeToken)] >=
                100 ether
            ) {
                stakeToken.mint(depositors[user], 5000 ether);
            }
        }
    }

    //a feature we could use to improve the contract later on!!
    function isTokenSupported(address _token) public returns (bool) {
        for (uint256 token = 0; token < supportedTokens.length; token++) {
            if (supportedTokens[token] == _token) {
                return true;
            }
        }
        return false;
    }

}
