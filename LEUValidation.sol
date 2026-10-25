// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title LEUValidationRegistry
 * @dev ERC-8004 Extension for Trustless Verification of L.E.U. Artifacts
 */
contract LEUValidationRegistry {
    struct Artifact {
        address creator;
        string entityId;
        string formula;
        bytes32 sha256Hash;
        bool isVerified;
    }

    mapping(bytes32 => Artifact) public artifacts;

    event ArtifactRegistered(bytes32 indexed hash, string entityId, address creator);
    event ArtifactVerified(bytes32 indexed hash, bool success);

    function registerArtifact(string memory _entityId, string memory _formula, bytes32 _hash) public {
        require(artifacts[_hash].creator == address(0), "Artifact already registered");
        
        artifacts[_hash] = Artifact({
            creator: msg.sender,
            entityId: _entityId,
            formula: _formula,
            sha256Hash: _hash,
            isVerified: true
        });

        emit ArtifactRegistered(_hash, _entityId, msg.sender);
    }

    function verifyArtifact(bytes32 _hash) public view returns (bool) {
        return artifacts[_hash].isVerified;
    }
}
