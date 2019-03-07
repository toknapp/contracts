from web3 import Web3
from pycontracts import contracts
from pycontracts.forward import Forward

class ForwardSolidity(Forward):
    def __init__(self, contract, owner = None):
        self.contract = contract
        super().__init__(contract.address)
        self._owner = owner

    @staticmethod
    def wrap(w3, address, owner = None):
        return ForwardSolidity(
            contract = w3.eth.contract(
                address = address,
                abi = contracts['Forward']['abi'],
            ),
            owner = owner
        )

    @staticmethod
    def deploy(w3, owner, originator = None):
        c = w3.eth.contract(
            bytecode = contracts['Forward']['deploy'],
            abi = contracts['Forward']['abi'],
        )

        tx_hash = c.constructor(owner).transact({
            'from': originator or w3.eth.defaultAccount,
        })
        r = w3.eth.waitForTransactionReceipt(tx_hash)
        return ForwardSolidity.wrap(w3, r.contractAddress, owner = owner)

    @property
    def owner(self):
        if not self._owner:
            self._owner = self.contract.functions.getOwner().call()
        return self._owner

    def nonce(self):
        return self.contract.functions.getNonce().call()

    def transact(self, call, originator):
        return self.contract.functions.forward(
            27 + call.signature.v,
            call.signature.r.to_bytes(32, 'big'),
            call.signature.s.to_bytes(32, 'big'),
            call.target, call.value, call.data
        ).transact({ 'from': originator })
