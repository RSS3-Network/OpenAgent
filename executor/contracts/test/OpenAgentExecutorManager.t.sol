// SPDX-License-Identifier: MIT
// solhint-disable comprehensive-interface,no-console
pragma solidity 0.8.18;

import {CommonTest} from "./helpers/CommonTest.sol";
import {Test} from "forge-std/Test.sol";
// import {console2 as console} from "forge-std/console2.sol";
import {Utils} from "./helpers/Utils.sol";
import {
    OpenAgentExecutorManager__InValidUserId,
    OpenAgentExecutorManager__InValidExecutorId,
    OpenAgentExecutorManager__NoRoleToCreateExecutor
} from "../src/Error.sol";
import {OpenAgentExecutorManager} from "../src/OpenAgentExecutorManager.sol";
import {OpenAgentExecutor} from "../src/OpenAgentExecutor.sol";
import {TransparentUpgradeableProxy} from "../src/upgradeability/TransparentUpgradeableProxy.sol";
import {Strings} from "@openzeppelin/contracts/utils/Strings.sol";

contract OpenAgentExecutorManagerTest is CommonTest {
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

    /// @notice Emitted when a executor is created.
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    function setUp() public {
        _setUp();
    }

    function testSetupStates() public {
        // check `DEFAULT_ADMIN_ROLE` role
        assertEq(_manager.hasRole(DEFAULT_ADMIN_ROLE, admin), true);
        assertEq(_manager.getRoleMemberCount(DEFAULT_ADMIN_ROLE), 1);
        assertEq(_manager.getRoleMember(DEFAULT_ADMIN_ROLE, 0), admin);

        bytes32 v = vm.load(address(_manager), bytes32(uint256(3)));
        v = vm.load(address(_manager), bytes32(0));
        assertEq(uint256(v), uint256(1)); // initialize version
    }

    function testInitialize() public {
        OpenAgentExecutorManager managerImpl = new OpenAgentExecutorManager();
        TransparentUpgradeableProxy proxy = new TransparentUpgradeableProxy(
            address(managerImpl),
            proxyAdmin,
            ""
        );
        OpenAgentExecutorManager(payable(address(proxy))).initialize(admin);

        bytes32 v = vm.load(address(proxy), bytes32(uint256(3)));

        v = vm.load(address(proxy), bytes32(0));
        assertEq(uint256(v), uint256(1)); // initialize version
    }

    function testInitializeFail() public {
        OpenAgentExecutorManager newImpl = new OpenAgentExecutorManager();
        // upgrade
        vm.prank(proxyAdmin);
        TransparentUpgradeableProxy(payable(address(_manager))).upgradeTo(address(newImpl));

        vm.expectRevert(abi.encodePacked("Initializable: contract is already initialized"));
        _manager.initialize(admin);
    }

    function testFund() public {
        // fund
        vm.deal(admin, 1 ether);
        vm.prank(admin);
        _manager.fund{value: 1 ether}();

        // check balance
        assertEq(address(_manager).balance, 1 ether);
        assertEq(admin.balance, 0);
    }

    function testCreateExecutor(uint256 userId) public {
        vm.assume(userId > 0 && userId < 1000);

        // create executor
        expectEmit();
        emit OwnershipTransferred(address(0), address(_manager));
        emit ExecutorCreated(userId, 1, address(0xffD4505B3452Dc22f8473616d50503bA9E1710Ac));
        vm.prank(admin);
        (, address executorAddr) = _manager.createExecutor(userId);

        // check executor index
        assertEq(_manager.getExecutorIndex(), 1);
        assertEq(_manager.getExecutorAddr(userId, 1), executorAddr);
    }

    function testDeposit(uint256 userId, uint256 amount) public {
        vm.assume(userId > 0 && userId < 1000);
        vm.assume(amount > 10 && amount < 1000);
        vm.prank(admin);
        (, address executorAddr) = _manager.createExecutor(userId);

        // deposit
        vm.deal(address(_manager), 1 ether);
        vm.expectEmit();
        emit TokensDeposited(executorAddr, amount, address(0));
        vm.prank(admin);
        _manager.deposit(userId, 1, address(0), amount);

        uint256 nativeBalance = _manager.getNativeTokenBalance(userId, 1);

        // check balance
        assertEq(address(_manager).balance, 1 ether - amount);
        assertEq(nativeBalance, amount);
    }

    function testWithdrawNativeToken(uint256 userId, uint256 amount) public {
        vm.assume(userId > 0 && userId < 1000);
        vm.assume(amount > 10 && amount < 1000);
        vm.prank(admin);
        (, address executorAddr) = _manager.createExecutor(userId);

        // fund executor
        vm.deal(executorAddr, amount);

        // check balance before withdraw
        uint256 nativeBalanceBefore = _manager.getNativeTokenBalance(userId, 1);
        assertEq(nativeBalanceBefore, amount);

        // withdraw
        vm.prank(admin);
        _manager.withdraw(userId, 1, payable(address(admin)), address(0), amount);

        uint256 nativeBalanceAfter = _manager.getNativeTokenBalance(userId, 1);
        assertEq(nativeBalanceAfter, 0);
        assertEq(address(admin).balance, amount);
    }

    function testTransferNativeToken(uint256 userId, uint256 amount) public {
        vm.assume(userId > 0 && userId < 1000);
        vm.assume(amount > 10 && amount < 1000);
        vm.prank(admin);
        (, address executorAddr1) = _manager.createExecutor(userId);

        // fund executor
        vm.deal(executorAddr1, amount);

        // check balance before withdraw
        uint256 nativeBalanceBefore = _manager.getNativeTokenBalance(userId, 1);
        assertEq(nativeBalanceBefore, amount);

        vm.prank(admin);
        _manager.createExecutor(userId);

        // transfer native token
        vm.deal(address(_manager), 1 ether);
        vm.prank(admin);
        _manager.transfer(userId, 1, userId, 2, address(0), amount);

        uint256 nativeBalanceAddr1 = _manager.getNativeTokenBalance(userId, 1);
        uint256 nativeBalanceAddr2 = _manager.getNativeTokenBalance(userId, 2);

        assertEq(nativeBalanceAddr1, 0);
        assertEq(nativeBalanceAddr2, amount);
    }

    function testTransferERC20Token(uint256 userId, uint256 amount) public {
        vm.assume(userId > 0 && userId < 1000);
        vm.assume(amount > 10 && amount < 1000);
        vm.prank(admin);
        (, address executorAddr1) = _manager.createExecutor(userId);

        // fund executor
        token.transfer(executorAddr1, amount);

        // check balance before
        uint256 erc20Balance = token.balanceOf(executorAddr1);
        assertEq(erc20Balance, amount);

        vm.prank(admin);
        (, address executorAddr2) = _manager.createExecutor(userId);

        vm.prank(admin);
        _manager.transfer(userId, 1, userId, 2, address(token), amount);

        uint256 erc20BalanceAddr1 = token.balanceOf(executorAddr1);
        uint256 erc20BalanceAddr2 = token.balanceOf(executorAddr2);

        assertEq(erc20BalanceAddr1, 0);
        assertEq(erc20BalanceAddr2, amount);
    }

    function testWithdrawERC20Token(uint256 userId, uint256 amount) public {
        vm.assume(userId > 0 && userId < 1000);
        vm.assume(amount > 10 && amount < 1000);
        vm.prank(admin);
        (, address executorAddr1) = _manager.createExecutor(userId);

        // fund executor
        token.transfer(executorAddr1, amount);

        // check balance before
        uint256 erc20Balance = token.balanceOf(executorAddr1);
        assertEq(erc20Balance, amount);

        vm.prank(admin);
        _manager.withdraw(userId, 1, payable(address(bob)), address(token), amount);

        uint256 erc20BalanceAddr1 = token.balanceOf(executorAddr1);
        uint256 erc20BalanceAddr2 = token.balanceOf(bob);

        assertEq(erc20BalanceAddr1, 0);
        assertEq(erc20BalanceAddr2, amount);
    }

    function testCreateMultipleExecutor4SingleUser(uint256 userId) public {
        vm.assume(userId > 0 && userId < 1000);

        // create executor
        expectEmit();
        emit OwnershipTransferred(address(0), address(_manager));
        emit ExecutorCreated(userId, 1, address(0xffD4505B3452Dc22f8473616d50503bA9E1710Ac));
        vm.prank(admin);
        (, address executorAddr1) = _manager.createExecutor(userId);
        // check executor index
        assertEq(_manager.getExecutorIndex(), 1);
        assertEq(_manager.getExecutorAddr(userId, 1), executorAddr1);

        expectEmit();
        emit OwnershipTransferred(address(0), address(_manager));
        emit ExecutorCreated(userId, 2, address(0x8d2C17FAd02B7bb64139109c6533b7C2b9CADb81));
        vm.prank(admin);
        (, address executorAddr2) = _manager.createExecutor(userId);

        // check executor index
        assertEq(_manager.getExecutorIndex(), 2);
        assertEq(_manager.getExecutorAddr(userId, 2), executorAddr2);
    }

    function testCreateExecutorFailed(uint256 userId) public {
        // Case 1: no role to invoke `createExecutor`
        vm.assume(userId > 0 && userId < 1000);
        // create executor
        vm.expectRevert(
            abi.encodeWithSelector(
                OpenAgentExecutorManager__NoRoleToCreateExecutor.selector,
                address(alice)
            )
        );
        vm.prank(alice);
        _manager.createExecutor(userId);

        // check executor index
        assertEq(_manager.getExecutorIndex(), 0);

        // Case 2: userId is 0
        userId = 0;
        // create executor
        vm.expectRevert(
            abi.encodeWithSelector(OpenAgentExecutorManager__InValidUserId.selector, userId)
        );
        vm.prank(admin);
        _manager.createExecutor(userId);

        // check executor index
        assertEq(_manager.getExecutorIndex(), 0);
    }

    function testGrantRole() public {
        // grant `DEFAULT_ADMIN_ROLE` to bob
        vm.prank(admin);
        _manager.grantRole(DEFAULT_ADMIN_ROLE, bob);
        assertEq(_manager.hasRole(DEFAULT_ADMIN_ROLE, bob), true);
        assertEq(_manager.getRoleMemberCount(DEFAULT_ADMIN_ROLE), 2);
        assertEq(_manager.getRoleMember(DEFAULT_ADMIN_ROLE, 1), bob);
    }

    function testGrantRoleFail() public {
        // case 1: caller has no `DEFAULT_ADMIN_ROLE` to grant `DEFAULT_ADMIN_ROLE` role
        vm.expectRevert(
            abi.encodePacked(
                "AccessControl: account ",
                Strings.toHexString(alice),
                " is missing role ",
                Strings.toHexString(uint256(DEFAULT_ADMIN_ROLE), 32)
            )
        );
        vm.prank(alice);
        _manager.grantRole(DEFAULT_ADMIN_ROLE, bob);
    }

    function testRenounceRole() public {
        // grant `DEFAULT_ADMIN_ROLE` to bob
        vm.prank(admin);
        _manager.grantRole(DEFAULT_ADMIN_ROLE, bob);
        // bob renounce `DEFAULT_ADMIN_ROLE` for himself
        vm.prank(bob);
        _manager.renounceRole(DEFAULT_ADMIN_ROLE, bob);
        assertEq(_manager.hasRole(DEFAULT_ADMIN_ROLE, bob), false);
        assertEq(_manager.getRoleMemberCount(DEFAULT_ADMIN_ROLE), 1);
    }

    function testRenounceRoleFail() public {
        // grant role to bob
        vm.prank(admin);
        _manager.grantRole(DEFAULT_ADMIN_ROLE, bob);

        // admin can't renounce `COLLECTOR_ROLE' for bob
        vm.expectRevert("AccessControl: can only renounce roles for self");
        vm.prank(admin);
        _manager.renounceRole(DEFAULT_ADMIN_ROLE, bob);
    }

    function testRevokeRole() public {
        // grant role to bob
        vm.prank(admin);
        _manager.grantRole(DEFAULT_ADMIN_ROLE, bob);
        assertEq(_manager.hasRole(DEFAULT_ADMIN_ROLE, bob), true);

        // renounce role
        vm.prank(admin);
        _manager.revokeRole(DEFAULT_ADMIN_ROLE, bob);

        // check role
        assertEq(_manager.hasRole(DEFAULT_ADMIN_ROLE, bob), false);
    }

    function testRevokeRoleFail() public {
        // grant role to bob
        vm.prank(admin);
        _manager.grantRole(DEFAULT_ADMIN_ROLE, bob);
        assertEq(_manager.hasRole(DEFAULT_ADMIN_ROLE, bob), true);

        // revoke role
        // bob has no `DEFAULT_ADMIN_ROLE`, so he can't revoke role
        vm.expectRevert(
            abi.encodePacked(
                "AccessControl: account ",
                Strings.toHexString(alice),
                " is missing role ",
                Strings.toHexString(uint256(DEFAULT_ADMIN_ROLE), 32)
            )
        );
        vm.prank(alice);
        _manager.revokeRole(DEFAULT_ADMIN_ROLE, bob);

        // check role
        assertEq(_manager.hasRole(DEFAULT_ADMIN_ROLE, bob), true);
    }
}
