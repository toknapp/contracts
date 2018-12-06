Upvest's smart contracts
========================

Forwarding contract
-------------------

* [Solidity implementation](src/Forward.sol)
* [Some tests](scala/src/test/scala/ForwardSpec.scala) (using `ganache-cli`, `web3j` and `ScalaTest`)

### Pseudo implementation


```python
def forward(self, sig, target, value, input):
    assert(ecrecover(keccak256(self.address + self.nonce + target + value + input), sig) == self.owner)
    self.nonce += 1
    return call(target, value, input)
```
