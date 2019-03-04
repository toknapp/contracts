from pycontracts import contracts
from eth_keys import keys

def contract(w3, address):
    return Forward(
        w3.eth.contract(
            address = address,
            abi = contracts['Forward']['abi']
        )
    )

def deploy(w3, owner, originator = None):
    c = w3.eth.contract(
        bytecode = contracts['Forward']['code'],
        abi = contracts['Forward']['abi'],
    )

    tx_hash = c.constructor(owner).transact({
        'from': originator or w3.eth.defaultAccount,
    })
    r = w3.eth.waitForTransactionReceipt(tx_hash)
    return contract(w3, r.contractAddress)


class Forward:
    def __init__(self, contract):
        self.address = contract.address
        self.contract = contract
        self._owner = None

    @property
    def owner(self):
        if not self._owner:
            self._owner = self.contract.functions.getOwner().call()

        return self._owner

    def nonce(self):
        return self.contract.functions.getNonce().call()
