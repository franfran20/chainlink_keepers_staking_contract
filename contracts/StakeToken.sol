//SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";


contract StakeToken is ERC20, Ownable {
    uint256 public s_totalSupply = 1000000 ether;
    constructor(string memory name, string memory symbol) ERC20(name, symbol){
        _mint(msg.sender, s_totalSupply);
    }

    function mint(address _to, uint256 _amount) external onlyOwner{
        _mint(_to, _amount);
    }
}