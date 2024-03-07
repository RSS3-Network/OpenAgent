// SPDX-License-Identifier: MIT

pragma solidity 0.8.18;

/// @dev Invalid User Id
error OpenAgentWalletManager__InValidUserId(uint256 userId);

/// @dev Invalid Wallet Id
error OpenAgentWalletManager__InValidWalletId(uint256 walletId);

/// @dev No Role To Create Wallet
error OpenAgentWalletManager__NoRoleToCreateWallet(address sender);
