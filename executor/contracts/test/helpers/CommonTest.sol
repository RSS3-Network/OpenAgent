// SPDX-License-Identifier: MIT
// solhint-disable comprehensive-interface
pragma solidity 0.8.18;

import {OpenAgentToken} from "../../src/mocks/OpenAgentToken.sol";
import {OpenAgentExecutorManager} from "../../src/OpenAgentExecutorManager.sol";
import {
    TransparentUpgradeableProxy
} from "../../src/upgradeability/TransparentUpgradeableProxy.sol";
import {Utils} from "./Utils.sol";

contract CommonTest is Utils {
    OpenAgentToken public token;
    OpenAgentExecutorManager internal _manager;

    address public constant proxyAdmin = address(0x777);
    address public constant admin = address(0x999999999999999999999999999999);

    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");

    uint256 public constant alicePrivateKey = 0x1111;
    uint256 public constant bobPrivateKey = 0x2222;
    uint256 public constant carolPrivateKey = 0x3333;
    uint256 public constant dickPrivateKey = 0x4444;
    uint256 public constant erikPrivateKey = 0x5555;
    address public constant dave = address(0x444);
    address public constant eve = address(0x555);
    address public constant frank = address(0x666);
    bytes32 public constant DEFAULT_ADMIN_ROLE = 0x00;
    uint256 public constant initialAmount = 1e9 ether;

    address public alice = vm.addr(alicePrivateKey);
    address public bob = vm.addr(bobPrivateKey);
    address public carol = vm.addr(carolPrivateKey);
    address public dick = vm.addr(dickPrivateKey);
    address public erik = vm.addr(erikPrivateKey);

    function _setUp() internal {
        // deploy web3Entry related contracts
        _deployContracts();
    }

    function _deployContracts() internal {
        // deploy token
        token = new OpenAgentToken();
        // deploy and init OpenAgentExecutorManager contract
        OpenAgentExecutorManager managerImpl = new OpenAgentExecutorManager();
        TransparentUpgradeableProxy proxy = new TransparentUpgradeableProxy(
            address(managerImpl),
            proxyAdmin,
            abi.encodeWithSignature("initialize(address)", admin)
        );
        _manager = OpenAgentExecutorManager(payable(address(proxy)));
    }
}
