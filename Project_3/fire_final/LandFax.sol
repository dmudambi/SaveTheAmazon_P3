pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/drafts/Counters.sol";

contract LandFax is ERC721Full {

    constructor() ERC721Full("LandToken", "RAIN") public { }

    using Counters for Counters.Counter;
    Counters.Counter token_ids;

    struct Land {
        string LatLon;
        uint fire;
    }

    mapping(uint => Land) public lands;

    event fire(uint token_id);

    function registerLand(address owner, string memory LatLon, string memory token_uri) public returns(uint) {
        token_ids.increment();
        uint token_id = token_ids.current();

        _mint(owner, token_id);
        _setTokenURI(token_id, token_uri);

        lands[token_id] = Land(LatLon, 0);

        return token_id;
    }

    function reportFire(uint token_id) public returns(uint) {
        lands[token_id].fire += 1;

        // Permanently associates the report_uri with the token_id on-chain via Events for a lower gas-cost than storing directly in the contract's storage.
        emit fire(token_id);

        return lands[token_id].fire;
    }
}