// SPDX-License-Identifier: MIT
pragma solidity 0.8.18;

interface IOpenAgentExecutorManager {
    /**
     * @notice Initializes the OpenAgentExecutorManager, setting the admin address.
     * @param admin The address to be granted as admin.
     */
    function initialize(address admin) external;

    /**
     * @notice Fund the contract with native tokens.
     */
    function fund() external payable;

    /**
     * @notice Creates a new user executor.
     * @dev Emits a {ExecutorCreated} event.
     * @param userId The ID of the user.
     * @return executorId The ID of the executor.
     * @return executorAddr The address of the executor.
     */
    function createExecutor(uint256 userId) external returns (uint256 executorId, address executorAddr);

    /**
     * @notice Deposits tokens to the openAgent executor contract.
     * @dev Emits a {TokensDeposit} event.
     * @param userId The ID of the user.
     * @param executorId The ID of the executor.
     * @param token The token address.
     * @param amount The amount of tokens to withdraw.
     */
    function deposit(uint256 userId, uint256 executorId, address token, uint256 amount) external;

    /**
     * @notice Withdraws tokens from the openAgent executor contract.
     * @dev Emits a {TokensWithdrawn} event.
     * @param userId The ID of the user.
     * @param executorId The ID of the executor.
     * @param to The address to withdraw tokens to.
     * @param token The token address.
     * @param amount The amount of tokens to withdraw.
     */
    function withdraw(
        uint256 userId,
        uint256 executorId,
        address payable to,
        address token,
        uint256 amount
    ) external;

    /**
     * @notice Transfer tokens from one executor to another.
     * @dev Emits a {TokensTransferred} event.
     * @param fromUserId The ID of the user to transfer tokens from.
     * @param fromExecutorId The ID of the executor to transfer tokens from.
     * @param toUserId The ID of the user to transfer tokens to.
     * @param toExecutorId The ID of the executor to transfer tokens to.
     * @param token The token address.
     * @param amount The amount of tokens to transfer.
     */
    function transfer(
        uint256 fromUserId,
        uint256 fromExecutorId,
        uint256 toUserId,
        uint256 toExecutorId,
        address token,
        uint256 amount
    ) external;

    /**
     * @notice Returns the balance of a user in the openAgent executor contract.
     * @param userId The ID of the user.
     * @param executorId The ID of the executor.
     * @return nativeBalance The balance of the user.
     */
    function getNativeTokenBalance(
        uint256 userId,
        uint256 executorId
    ) external view returns (uint256 nativeBalance);

    /**
     * @notice Returns the balance of a user in the openAgent executor contract.
     * @param userId The ID of the user.
     * @param executorId The ID of the executor.
     * @param token The token address.
     * @return tokenBalance The balance of the user.
     */
    function getTokenBalance(
        uint256 userId,
        uint256 executorId,
        address token
    ) external view returns (uint256 tokenBalance);

    /**
     * @notice getExecutorAddr from a user.
     * @param userId The ID of the user.
     * @param executorId The ID of the executor.
     */
    function getExecutorAddr(uint256 userId, uint256 executorId) external view returns (address);

    /**
     * @notice getLatestExecutorId
     */
    function getExecutorIndex() external view returns (uint256);
}
