pragma solidity ^0.5.11;

contract Mock {
    function echo(uint256 i) public pure returns (uint256) {
        return i;
    }

    function maybe_fail(bool yay, string memory s) public pure returns (string memory) {
        if(yay) {
            return s;
        } else {
            revert(s);
        }
    }
}
