pragma solidity ^0.5.11;

contract State {
    mapping (address => uint256) private v;

    function fetch() public view returns (uint256) {
        return v[msg.sender];
    }

    function fetch(address a) public view returns (uint256) {
        return v[a];
    }

    function set(uint256 i) public {
        v[msg.sender] = i;
    }
}
