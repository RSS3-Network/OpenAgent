// SPDX-License-Identifier: MIT
pragma solidity 0.8.18;

import "./interfaces/IOpenAgentWalletManager.sol";
import "./interfaces/IOpenAgentWallet.sol";
import "./OpenAgentWallet.sol";
import {
    OpenAgentWalletManager__InValidUserId,
    OpenAgentWalletManager__InValidWalletId,
    OpenAgentWalletManager__NoRoleToCreateWallet
} from "./Error.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {Initializable} from "@openzeppelin/contracts/proxy/utils/Initializable.sol";
import {AccessControlEnumerable} from "@openzeppelin/contracts/access/AccessControlEnumerable.sol";

/**
 * @title OpenAgentWalletManager
 * @notice The OpenAgentWalletManager contract is used to generate and manage users' wallets.
 */
contract OpenAgentWalletManager is IOpenAgentWalletManager, Initializable, AccessControlEnumerable {
    using SafeERC20 for IERC20;

    mapping(uint256 => mapping(uint256 => address)) internal _wallets;
    uint256 internal _walletIndex;

    // events
    /// @notice Emitted when a wallet is created.
    event WalletCreated(
        uint256 indexed userId,
        uint256 indexed walletId,
        address indexed walletAddr
    );
    /// @notice Emitted when tokens are deposited.
    event TokensDeposited(address indexed to, uint256 indexed amount, address token);
    /// @notice Emitted when tokens are withdrawn.
    event TokensWithdrawn(
        address indexed from,
        address indexed to,
        uint256 indexed amount,
        address token
    );
    /// @notice Emitted when tokens are transferred.
    event TokensTransferred(
        address indexed from,
        address indexed to,
        uint256 indexed amount,
        address token
    );

    modifier validUserId(uint256 userId) {
        if (userId <= 0) revert OpenAgentWalletManager__InValidUserId(userId);
        _;
    }

    modifier validWalletId(uint256 walletId) {
        if (walletId <= 0) revert OpenAgentWalletManager__InValidWalletId(walletId);
        _;
    }

    modifier onlyAdmin() {
        if (!hasRole(DEFAULT_ADMIN_ROLE, msg.sender))
            revert OpenAgentWalletManager__NoRoleToCreateWallet(msg.sender);
        _;
    }

    constructor() {
        _disableInitializers();
    }

    /// @inheritdoc IOpenAgentWalletManager
    function initialize(address admin) external override initializer {
        // grants `DEFAULT_ADMIN_ROLE`
        _setupRole(DEFAULT_ADMIN_ROLE, admin);
    }

    /// @inheritdoc IOpenAgentWalletManager
    // solhint-disable-next-line no-empty-blocks
    function fund() external payable override {}

    /// @inheritdoc IOpenAgentWalletManager
    function createWallet(
        uint256 userId
    ) public override validUserId(userId) onlyAdmin returns (uint256 walletId, address walletAddr) {
        IOpenAgentWallet openAgentWallet = new OpenAgentWallet();
        walletAddr = address(openAgentWallet);
        _walletIndex++;
        _wallets[userId][_walletIndex] = walletAddr;
        walletId = _walletIndex;
        emit WalletCreated(userId, _walletIndex, walletAddr);
    }

    /// @inheritdoc IOpenAgentWalletManager
    function deposit(
        uint256 userId,
        uint256 walletId,
        address token,
        uint256 amount
    ) public override validUserId(userId) validWalletId(walletId) onlyAdmin {
        address sender = msg.sender;
        address openAgentWalletAddr = _wallets[userId][walletId];

        IOpenAgentWallet openAgentWallet = IOpenAgentWallet(payable(openAgentWalletAddr));

        IOpenAgentWallet.Call[] memory calls = new IOpenAgentWallet.Call[](1);
        if (token != address(0)) {
            calls[0] = IOpenAgentWallet.Call({
                target: address(token),
                callData: abi.encodeWithSelector(
                    IERC20.transferFrom.selector,
                    sender,
                    openAgentWalletAddr,
                    amount
                )
            });
            openAgentWallet.aggregate(calls);
            emit TokensDeposited(openAgentWalletAddr, amount, token);
        } else {
            openAgentWallet.aggregate{value: amount}(calls);
            emit TokensDeposited(openAgentWalletAddr, amount, address(0));
        }
    }

    /// @inheritdoc IOpenAgentWalletManager
    function withdraw(
        uint256 userId,
        uint256 walletId,
        address payable to,
        address token,
        uint256 amount
    ) public override validUserId(userId) validWalletId(walletId) onlyAdmin {
        address openAgentWalletAddr = _wallets[userId][walletId];

        IOpenAgentWallet openAgentWallet = IOpenAgentWallet(payable(openAgentWalletAddr));

        IOpenAgentWallet.Call[] memory calls = new IOpenAgentWallet.Call[](1);
        if (token != address(0)) {
            calls[0] = IOpenAgentWallet.Call({
                target: address(token),
                callData: abi.encodeWithSelector(IERC20.transfer.selector, to, amount)
            });
            openAgentWallet.aggregate(calls);
            emit TokensWithdrawn(openAgentWalletAddr, to, amount, token);
        } else {
            openAgentWallet.withdraw(to, amount);
            emit TokensWithdrawn(openAgentWalletAddr, to, amount, address(0));
        }
    }

    /// @inheritdoc IOpenAgentWalletManager
    function transfer(
        uint256 fromUserId,
        uint256 fromWalletId,
        uint256 toUserId,
        uint256 toWalletId,
        address token,
        uint256 amount
    )
        public
        override
        validUserId(fromUserId)
        validUserId(toUserId)
        validWalletId(fromWalletId)
        validWalletId(toWalletId)
        onlyAdmin
    {
        address fromOpenAgentWalletAddr = _wallets[fromUserId][fromWalletId];
        address toOpenAgentWalletAddr = _wallets[toUserId][toWalletId];

        IOpenAgentWallet fromOpenAgentWallet = IOpenAgentWallet(payable(fromOpenAgentWalletAddr));

        IOpenAgentWallet.Call[] memory calls = new IOpenAgentWallet.Call[](1);
        if (token != address(0)) {
            calls[0] = IOpenAgentWallet.Call({
                target: address(token),
                callData: abi.encodeWithSelector(
                    IERC20.transfer.selector,
                    toOpenAgentWalletAddr,
                    amount
                )
            });

            fromOpenAgentWallet.aggregate(calls);
            emit TokensTransferred(fromOpenAgentWalletAddr, toOpenAgentWalletAddr, amount, token);
        } else {
            fromOpenAgentWallet.withdraw(payable(toOpenAgentWalletAddr), amount);
            emit TokensTransferred(fromOpenAgentWalletAddr, toOpenAgentWalletAddr, amount, token);
        }
    }

    /// @inheritdoc IOpenAgentWalletManager
    function getNativeTokenBalance(
        uint256 userId,
        uint256 walletId
    )
        public
        view
        override
        validUserId(userId)
        validWalletId(walletId)
        returns (uint256 nativeBalance)
    {
        return _wallets[userId][walletId].balance;
    }

    /// @inheritdoc IOpenAgentWalletManager
    function getTokenBalance(
        uint256 userId,
        uint256 walletId,
        address token
    )
        public
        view
        override
        validUserId(userId)
        validWalletId(walletId)
        returns (uint256 tokenBalance)
    {
        return (IERC20(token).balanceOf(_wallets[userId][walletId]));
    }

    /// @inheritdoc IOpenAgentWalletManager
    function getWalletAddr(
        uint256 userId,
        uint256 walletId
    ) public view override validUserId(userId) validWalletId(walletId) returns (address) {
        return _wallets[userId][walletId];
    }

    /// @inheritdoc IOpenAgentWalletManager
    function getWalletIndex() public view override returns (uint256) {
        return _walletIndex;
    }
}
