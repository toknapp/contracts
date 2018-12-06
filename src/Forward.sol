pragma solidity ^0.4.24;

contract Forward {
    address owner;

    constructor(address _owner) public {
        owner = _owner;
    }

    // TODO: value can be arbitrarily large?
    function forward(
        uint8 v, bytes32 r, bytes32 s,
        address target, uint256 value, bytes i
    ) public payable returns (bool) {
        //bytes memory sd = new bytes(20+32+i.length);
        //assembly { mstore(add(sd, 32), target) }

        require(ecrecover(keccak256(i), v, r, s) == owner, "invalid signature");

        // TODO: verify signature
        // TODO: verify nonce (maybe include tx originator and tx nonce in the signature?)
        // TODO: increase nonce (then this would be unnecessary, and there's no need to have a separate call to get the nonce)
        // TODO: handle output data? maybe annoying to do in solidity
        return target.call.value(value)(i);
    }
}
