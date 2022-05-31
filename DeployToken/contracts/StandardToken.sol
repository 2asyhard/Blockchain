// contracts/StandardToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract StandardToken is ERC20 {
    // wei
    constructor(uint256 initialSupply) ERC20("MyToken", "MT") {
        _mint(msg.sender, initialSupply);
    }
}

