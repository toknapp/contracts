Upvest's smart contracts
========================

[![CircleCI](https://circleci.com/gh/toknapp/contracts/tree/master.svg?style=svg)](https://circleci.com/gh/toknapp/contracts/tree/master)

Forwarding contract
-------------------
### Background (the why)
While thinking about how to allow users to manage their ERC20 tokens in our
platform without knowing anything about the Ethereum blockchain (including
having to hold any ether), we stumbled upon the idea that what's really needed
is for us to be the transaction originator (paying the gas) while having an
intermediate contract talking to the ERC20 contracts (so that it will be the
`msg.sender` in the call).

#### References
* [EIP 86](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-86.md#rationale)

### The code (the how)
* [Solidity implementation](src/Forward.sol)
* [Bare-metal EVM implementation](src/further.runtime.evm)
* [Python abstraction](pycontracts/forward.py) with implementations:
  - [Solidity contract wrapper](pycontracts/forward_solidity.py)
  - [Bare-metal contract wrapper](pycontracts/further.py)
* [and their tests](pycontracts/tests/test_forward.py)

#### Pseudo implementation
```python
def forward(self, sig, target, value, input):
    assert(ecrecover(keccak256(self.address + target + value + self.nonce + input), sig) == self.owner)
    self.nonce += 1
    return call(target, value, input)
```

Notice the fact that the contracts address is included in the signature, in
order to prevent the transaction from being replayed to a cloned contract.
Consider the scenario with a voting contract: the user votes through his
forwarding contract, then without this check a malicious user can deploy copies
of the forwarding contract (with the same `owner`) and replay the voting call.
