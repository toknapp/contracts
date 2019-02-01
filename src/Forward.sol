pragma solidity ^0.4.24;

contract Forward {
    address public owner;
    uint256 public nonce;

    constructor(address _owner) public {
        require(_owner != address(0));
        owner = _owner;
    }

    function forward(
        uint8 v, bytes32 r, bytes32 s,
        address target, uint256 value, bytes input
    ) public payable {
        require(
            ecrecover(keccak256(abi.encodePacked(target, value, input)), v, r, s) == owner,
            "invalid signature"
        );

        nonce += 1;

        // TODO: handle output data? maybe annoying to do in solidity
        require(target.call.value(value)(input));
    }
    
    // TODO: withdraw functions for offboarding

    // allow receiving ETH
    function() external payable { }
}
