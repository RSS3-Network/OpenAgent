// SPDX-License-Identifier: MIT
// solhint-disable private-vars-leading-underscore,no-console
pragma solidity 0.8.18;

import {Script} from "forge-std/Script.sol";
import {console2 as console} from "forge-std/console2.sol";
import {stdJson} from "forge-std/StdJson.sol";

/// @title DeployConfig
/// @notice Represents the configuration required to deploy the system. It is expected
///         to read the file from JSON. A future improvement would be to have fallback
///         values if they are not defined in the JSON themselves.
contract DeployConfig is Script {
    string internal _json;

    uint256 public chainID;
    address public proxyAdminOwner;
    address public admin;
    address public manager;

    constructor(string memory _path) {
        console.log("DeployConfig: reading file %s", _path);
        try vm.readFile(_path) returns (string memory data) {
            _json = data;
        } catch {
            console.log(
                "Warning: unable to read config. Do not deploy unless you are not using config."
            );
            return;
        }

        chainID = stdJson.readUint(_json, "$.chainID");
        proxyAdminOwner = stdJson.readAddress(_json, "$.proxyAdminOwner");
        manager = stdJson.readAddress(_json, "$.manager");
    }
}
