// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title LEU Genesis Pass
 * @dev NFT d'acces pour l'ecosysteme L.E.U.
 * Fournit un acces API, des credits de generation et un droit de gouvernance.
 */
contract LEUGenesisPass {
    string public name = "L.E.U. Genesis Pass";
    string public symbol = "LEU-GP";
    uint256 public totalSupply = 0;
    uint256 public constant MAX_SUPPLY = 1000;
    uint256 public constant PRICE = 0.05 ether;

    address public owner;
    mapping(address => bool) public hasPass;
    mapping(uint256 => address) public tokenOwner;

    event PassMinted(address indexed owner, uint256 tokenId);
    event PassBurned(address indexed owner, uint256 tokenId);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not the contract owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    /**
     * @dev Mint un nouveau Genesis Pass.
     * Limite a 1000 pour garantir la rarete.
     */
    function mintPass() public payable {
        require(totalSupply < MAX_SUPPLY, "Max supply reached");
        require(msg.value >= PRICE, "Insufficient payment");
        require(!hasPass[msg.sender], "Already owns a pass");

        totalSupply++;
        hasPass[msg.sender] = true;
        tokenOwner[totalSupply] = msg.sender;

        emit PassMinted(msg.sender, totalSupply);
    }

    /**
     * @dev Verifie si une adresse detient un Pass.
     * Utilise par l'API L.E.U. pour autoriser les requetes.
     */
    function verifyAccess(address user) public view returns (bool) {
        return hasPass[user];
    }

    /**
     * @dev Retrait des fonds vers le createur.
     */
    function withdraw() public onlyOwner {
        (bool success, ) = owner.call{value: address(this).balance}("");
        require(success, "Transfer failed");
    }
}
