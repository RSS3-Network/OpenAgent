// SPDX-License-Identifier: MIT
pragma solidity 0.8.18;

interface IOpenAgentWalletManager {
    /**
     * @notice Initializes the OpenAgentWalletManager, setting the admin address.
     * @param admin The address to be granted as admin.
     */
    function initialize(address admin) external;

    /**
     * @notice Fund the contract with native tokens.
     */
    function fund() external payable;

    /**
     * @notice Creates a new user wallet.
     * @dev Emits a {WalletCreated} event.
     * @param userId The ID of the user.
     * @return walletId The ID of the wallet.
     * @return walletAddr The address of the wallet.
     */
    function createWallet(uint256 userId) external returns (uint256 walletId, address walletAddr);

    /**
     * @notice Deposits tokens to the openAgent wallet contract.
     * @dev Emits a {TokensDeposit} event.
     * @param userId The ID of the user.
     * @param walletId The ID of the wallet.
     * @param token The token address.
     * @param amount The amount of tokens to withdraw.
     */
    function deposit(uint256 userId, uint256 walletId, address token, uint256 amount) external;

    /**
     * @notice Withdraws tokens from the openAgent wallet contract.
     * @dev Emits a {TokensWithdrawn} event.
     * @param userId The ID of the user.
     * @param walletId The ID of the wallet.
     * @param to The address to withdraw tokens to.
     * @param token The token address.
     * @param amount The amount of tokens to withdraw.
     */
    function withdraw(
        uint256 userId,
        uint256 walletId,
        address payable to,
        address token,
        uint256 amount
    ) external;

    /**
     * @notice Transfer tokens from one wallet to another.
     * @dev Emits a {TokensTransferred} event.
     * @param fromUserId The ID of the user to transfer tokens from.
     * @param fromWalletId The ID of the wallet to transfer tokens from.
     * @param toUserId The ID of the user to transfer tokens to.
     * @param toWalletId The ID of the wallet to transfer tokens to.
     * @param token The token address.
     * @param amount The amount of tokens to transfer.
     */
    function transfer(
        uint256 fromUserId,
        uint256 fromWalletId,
        uint256 toUserId,
        uint256 toWalletId,
        address token,
        uint256 amount
    ) external;

    /**
     * @notice Returns the balance of a user in the openAgent wallet contract.
     * @param userId The ID of the user.
     * @param walletId The ID of the wallet.
     * @return nativeBalance The balance of the user.
     */
    function getNativeTokenBalance(
        uint256 userId,
        uint256 walletId
    ) external view returns (uint256 nativeBalance);

    /**
     * @notice Returns the balance of a user in the openAgent wallet contract.
     * @param userId The ID of the user.
     * @param walletId The ID of the wallet.
     * @param token The token address.
     * @return tokenBalance The balance of the user.
     */
    function getTokenBalance(
        uint256 userId,
        uint256 walletId,
        address token
    ) external view returns (uint256 tokenBalance);

    /**
     * @notice getWalletAddr from a user.
     * @param userId The ID of the user.
     * @param walletId The ID of the wallet.
     */
    function getWalletAddr(uint256 userId, uint256 walletId) external view returns (address);

    /**
     * @notice getLatestWalletId
     */
    function getWalletIndex() external view returns (uint256);
}
