Upvest's smart contracts
========================

Forwarding contract
-------------------

### Pseudo implementation

```python
def forward(sig, target, value, input):
    assert(ecrecover(sha3(this.address + this.nonce + target + value + input), sig) == owner)
    this.nonce += 1
    return call(target, value, input)
```
