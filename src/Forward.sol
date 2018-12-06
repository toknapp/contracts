pragma solidity ^0.4.24;

contract Forward {
    // TODO: value can be arbitrarily large?
    function forward(address target, uint256 v, bytes i)
        public payable returns (bool) {
            // TODO: verify signature
            // TODO: verify nonce (maybe include tx originator and tx nonce in the signature?)
            // TODO: increase nonce (then this would be unnecessary, and there's no need to have a separate call to get the nonce)
            // TODO: handle output data? maybe annoying to do in solidity
            return target.call.value(v)(i);
        }
}
