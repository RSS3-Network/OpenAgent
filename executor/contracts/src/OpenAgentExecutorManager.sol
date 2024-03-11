// SPDX-License-Identifier: MIT
pragma solidity 0.8.18;

import "./interfaces/IOpenAgentExecutorManager.sol";
import "./interfaces/IOpenAgentExecutor.sol";
import "./OpenAgentExecutor.sol";
import {
    OpenAgentExecutorManager__InValidUserId,
    OpenAgentExecutorManager__InValidExecutorId,
    OpenAgentExecutorManager__NoRoleToCreateExecutor
} from "./Error.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {Initializable} from "@openzeppelin/contracts/proxy/utils/Initializable.sol";
import {AccessControlEnumerable} from "@openzeppelin/contracts/access/AccessControlEnumerable.sol";

/**
 * @title OpenAgentExecutorManager
 * @notice The OpenAgentExecutorManager contract is used to generate and manage users' executors.
 */
contract OpenAgentExecutorManager is IOpenAgentExecutorManager, Initializable, AccessControlEnumerable {
    using SafeERC20 for IERC20;

    mapping(uint256 => mapping(uint256 => address)) internal _executors;
    uint256 internal _executorIndex;

    // events
    /// @notice Emitted when a executor is created.
    event ExecutorCreated(
        uint256 indexed userId,
        uint256 indexed executorId,
        address indexed executorAddr
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
        if (userId <= 0) revert OpenAgentExecutorManager__InValidUserId(userId);
        _;
    }

    modifier validExecutorId(uint256 executorId) {
        if (executorId <= 0) revert OpenAgentExecutorManager__InValidExecutorId(executorId);
        _;
    }

    modifier onlyAdmin() {
        if (!hasRole(DEFAULT_ADMIN_ROLE, msg.sender))
            revert OpenAgentExecutorManager__NoRoleToCreateExecutor(msg.sender);
        _;
    }

    constructor() {
        _disableInitializers();
    }

    /// @inheritdoc IOpenAgentExecutorManager
    function initialize(address admin) external override initializer {
        // grants `DEFAULT_ADMIN_ROLE`
        _setupRole(DEFAULT_ADMIN_ROLE, admin);
    }

    /// @inheritdoc IOpenAgentExecutorManager
    // solhint-disable-next-line no-empty-blocks
    function fund() external payable override {}

    /// @inheritdoc IOpenAgentExecutorManager
    function createExecutor(
        uint256 userId
    ) public override validUserId(userId) onlyAdmin returns (uint256 executorId, address executorAddr) {
        IOpenAgentExecutor openAgentExecutor = new OpenAgentExecutor();
        executorAddr = address(openAgentExecutor);
        _executorIndex++;
        _executors[userId][_executorIndex] = executorAddr;
        executorId = _executorIndex;
        emit ExecutorCreated(userId, _executorIndex, executorAddr);
    }

    /// @inheritdoc IOpenAgentExecutorManager
    function deposit(
        uint256 userId,
        uint256 executorId,
        address token,
        uint256 amount
    ) public override validUserId(userId) validExecutorId(executorId) onlyAdmin {
        address sender = msg.sender;
        address openAgentExecutorAddr = _executors[userId][executorId];

        IOpenAgentExecutor openAgentExecutor = IOpenAgentExecutor(payable(openAgentExecutorAddr));

        IOpenAgentExecutor.Call[] memory calls = new IOpenAgentExecutor.Call[](1);
        if (token != address(0)) {
            calls[0] = IOpenAgentExecutor.Call({
                target: address(token),
                callData: abi.encodeWithSelector(
                    IERC20.transferFrom.selector,
                    sender,
                    openAgentExecutorAddr,
                    amount
                )
            });
            openAgentExecutor.aggregate(calls);
            emit TokensDeposited(openAgentExecutorAddr, amount, token);
        } else {
            openAgentExecutor.aggregate{value: amount}(calls);
            emit TokensDeposited(openAgentExecutorAddr, amount, address(0));
        }
    }

    /// @inheritdoc IOpenAgentExecutorManager
    function withdraw(
        uint256 userId,
        uint256 executorId,
        address payable to,
        address token,
        uint256 amount
    ) public override validUserId(userId) validExecutorId(executorId) onlyAdmin {
        address openAgentExecutorAddr = _executors[userId][executorId];

        IOpenAgentExecutor openAgentExecutor = IOpenAgentExecutor(payable(openAgentExecutorAddr));

        IOpenAgentExecutor.Call[] memory calls = new IOpenAgentExecutor.Call[](1);
        if (token != address(0)) {
            calls[0] = IOpenAgentExecutor.Call({
                target: address(token),
                callData: abi.encodeWithSelector(IERC20.transfer.selector, to, amount)
            });
            openAgentExecutor.aggregate(calls);
            emit TokensWithdrawn(openAgentExecutorAddr, to, amount, token);
        } else {
            openAgentExecutor.withdraw(to, amount);
            emit TokensWithdrawn(openAgentExecutorAddr, to, amount, address(0));
        }
    }

    /// @inheritdoc IOpenAgentExecutorManager
    function transfer(
        uint256 fromUserId,
        uint256 fromExecutorId,
        uint256 toUserId,
        uint256 toExecutorId,
        address token,
        uint256 amount
    )
        public
        override
        validUserId(fromUserId)
        validUserId(toUserId)
        validExecutorId(fromExecutorId)
        validExecutorId(toExecutorId)
        onlyAdmin
    {
        address fromOpenAgentExecutorAddr = _executors[fromUserId][fromExecutorId];
        address toOpenAgentExecutorAddr = _executors[toUserId][toExecutorId];

        IOpenAgentExecutor fromOpenAgentExecutor = IOpenAgentExecutor(payable(fromOpenAgentExecutorAddr));

        IOpenAgentExecutor.Call[] memory calls = new IOpenAgentExecutor.Call[](1);
        if (token != address(0)) {
            calls[0] = IOpenAgentExecutor.Call({
                target: address(token),
                callData: abi.encodeWithSelector(
                    IERC20.transfer.selector,
                    toOpenAgentExecutorAddr,
                    amount
                )
            });

            fromOpenAgentExecutor.aggregate(calls);
            emit TokensTransferred(fromOpenAgentExecutorAddr, toOpenAgentExecutorAddr, amount, token);
        } else {
            fromOpenAgentExecutor.withdraw(payable(toOpenAgentExecutorAddr), amount);
            emit TokensTransferred(fromOpenAgentExecutorAddr, toOpenAgentExecutorAddr, amount, token);
        }
    }

    /// @inheritdoc IOpenAgentExecutorManager
    function getNativeTokenBalance(
        uint256 userId,
        uint256 executorId
    )
        public
        view
        override
        validUserId(userId)
        validExecutorId(executorId)
        returns (uint256 nativeBalance)
    {
        return _executors[userId][executorId].balance;
    }

    /// @inheritdoc IOpenAgentExecutorManager
    function getTokenBalance(
        uint256 userId,
        uint256 executorId,
        address token
    )
        public
        view
        override
        validUserId(userId)
        validExecutorId(executorId)
        returns (uint256 tokenBalance)
    {
        return (IERC20(token).balanceOf(_executors[userId][executorId]));
    }

    /// @inheritdoc IOpenAgentExecutorManager
    function getExecutorAddr(
        uint256 userId,
        uint256 executorId
    ) public view override validUserId(userId) validExecutorId(executorId) returns (address) {
        return _executors[userId][executorId];
    }

    /// @inheritdoc IOpenAgentExecutorManager
    function getExecutorIndex() public view override returns (uint256) {
        return _executorIndex;
    }
}
