pragma solidity ^0.4.24;

contract Forward {
    address private owner;
    uint256 private nonce;

    constructor(address _owner) public {
        owner = _owner;
        nonce = 0;
    }

    function forward(
        uint8 v, bytes32 r, bytes32 s,
        address target, uint256 value, bytes input
    ) public payable returns (bool) {
        require(
            ecrecover(keccak256(signingData(target, value, input)), v, r, s) == owner,
            "invalid signature lol"
        );

        nonce += 1;

        // TODO: handle output data? maybe annoying to do in solidity
        return target.call.value(value)(input);
    }

    function signingData(
        address target,
        uint256 value,
        bytes input
    ) public view returns (bytes) {
        bytes memory sd = new bytes(32+32+32+32+input.length);
        uint sd_;
        uint i_;
        address a = this;
        assembly {
            sd_ := add(sd, 32)
            i_ := add(input, 32)

            mstore(sd_, a)
            sd_ := add(sd_, 32)

            mstore(sd_, target)
            sd_ := add(sd_, 32)

            mstore(sd_, value)
            sd_ := add(sd_, 32)

            mstore(sd_, nonce_offset)
            sd_ := add(sd_, 32)
        }
        memcpy(sd_, i_, input.length);

        return sd;
    }

    // https://github.com/Arachnid/solidity-stringutils/blob/3c63f18245645ba600cae2191deba7221512f753/src/strings.sol#L45
    function memcpy(uint dest, uint src, uint len) private pure {
        // Copy word-length chunks while possible
        for(; len >= 32; len -= 32) {
            assembly {
                mstore(dest, mload(src))
            }
            dest += 32;
            src += 32;
        }

        // Copy remaining bytes
        uint mask = 256 ** (32 - len) - 1;
        assembly {
            let srcpart := and(mload(src), not(mask))
            let destpart := and(mload(dest), mask)
            mstore(dest, or(destpart, srcpart))
        }
    }

    function getNonce() public view returns (uint256) { return nonce; }
    function getOwner() public view returns (address) { return owner; }

    function() public payable { }
}
