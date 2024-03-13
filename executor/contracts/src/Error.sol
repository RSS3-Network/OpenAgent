// SPDX-License-Identifier: MIT

pragma solidity 0.8.18;

/// @dev Invalid User Id
error OpenAgentExecutorManager__InValidUserId(uint256 userId);

/// @dev Invalid Executor Id
error OpenAgentExecutorManager__InValidExecutorId(uint256 executorId);

/// @dev No Role To Create Executor
error OpenAgentExecutorManager__NoRoleToCreateExecutor(address sender);
