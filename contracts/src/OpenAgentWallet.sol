// SPDX-License-Identifier: MIT
pragma solidity 0.8.18;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./interfaces/IOpenAgentWallet.sol";

contract OpenAgentWallet is IOpenAgentWallet, Ownable {
    /// @inheritdoc IOpenAgentWallet
    // solhint-disable-next-line no-empty-blocks
    receive() external payable override {}

    /// @inheritdoc IOpenAgentWallet
    // solhint-disable-next-line no-empty-blocks
    fallback() external payable override {}

    /// @inheritdoc IOpenAgentWallet
    function aggregate(
        Call[] calldata calls
    ) public payable override onlyOwner returns (uint256 blockNumber, bytes[] memory returnData) {
        blockNumber = block.number;
        uint256 length = calls.length;
        returnData = new bytes[](length);
        Call calldata call;
        for (uint256 i = 0; i < length; ) {
            bool success;
            call = calls[i];
            // solhint-disable-next-line avoid-low-level-calls
            (success, returnData[i]) = call.target.call(call.callData);
            require(success, "aggregate call failed");
            unchecked {
                ++i;
            }
        }
    }

    /// @inheritdoc IOpenAgentWallet
    function withdraw(address payable to, uint256 amount) public override onlyOwner {
        (bool success, ) = to.call{value: amount}("");
        require(success, "withdraw failed");
    }
}
