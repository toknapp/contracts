pragma solidity ^0.4.24;

contract State {
    uint256 v;
    function get() public view returns (uint256) {
        return v;
    }
    function set(uint256 i) public {
        v = i;
    }
}
