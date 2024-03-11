//SPDX-License-Identifier: MIT

pragma solidity 0.8.18;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract OpenAgentToken is ERC20 {
    constructor() ERC20("OpenAgentToken", "CT") {
        _mint(msg.sender, 10000000000 * 10 ** 6);
    }

    function decimals() public view virtual override returns (uint8) {
        return 6;
    }
}
