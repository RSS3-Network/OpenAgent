// SPDX-License-Identifier: MIT
// solhint-disable private-vars-leading-underscore
pragma solidity 0.8.18;

/// @notice Chain IDs for the various networks.
library Chains {
    uint256 internal constant Mainnet = 1;
    uint256 internal constant OPMainnet = 10;
    uint256 internal constant Goerli = 5;
    uint256 internal constant Sepolia = 11155111;
    uint256 internal constant LocalDevNet = 31337;
}
