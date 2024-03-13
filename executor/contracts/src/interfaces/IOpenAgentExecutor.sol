// SPDX-License-Identifier: MIT
pragma solidity 0.8.18;

interface IOpenAgentExecutor {
    struct Call {
        address target;
        bytes callData;
    }

    /// @notice Receive function to allow the contract to receive native tokens
    receive() external payable;

    /// @notice Fallback function to allow the contract to receive native tokens
    fallback() external payable;

    /// @notice Backwards-compatible call aggregation with Multicall
    /// @param calls An array of Call structs
    /// @return blockNumber The block number where the calls were executed
    /// @return returnData An array of bytes containing the responses
    function aggregate(
        Call[] calldata calls
    ) external payable returns (uint256 blockNumber, bytes[] memory returnData);

    /// @notice Withdraw native tokens from the contract
    /// @param to The address to withdraw to
    /// @param amount The amount of native tokens to withdraw
    function withdraw(address payable to, uint256 amount) external;
}
