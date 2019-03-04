from pycontracts import contracts
from web3 import Web3

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

    def signing_data(self, target, value, data, nonce):
        return bytes(12) + Web3.toBytes(hexstr=self.address) \
            + bytes(12) + Web3.toBytes(hexstr=target) \
            + value.to_bytes(32, 'big') \
            + nonce.to_bytes(32, 'big') \
            + data

    def _build(self, private_key, target, value, data, nonce):
        if hasattr(data, 'buildTransaction'):
            t = data.buildTransaction({"nonce": 0, "gas": 0, "gasPrice": 0})
            data = Web3.toBytes(hexstr = t['data'])
            if not target:
                target = t['to']

        if nonce is None:
            nonce = self.nonce()

        sig = private_key.sign_msg(
            self.signing_data(
                target = target,
                value = value,
                data = data,
                nonce = nonce,
            )
        )

        return self.contract.functions.forward(
            27 + sig.v, sig.r.to_bytes(32, 'big'), sig.s.to_bytes(32, 'big'),
            target, value, data
        )

    def transact(self, private_key, originator, target = None, value = 0, data = b'', nonce = None):
        return self._build(private_key, target, value, data, nonce).transact({ 'from': originator })

    def call(self, private_key, target = None, value = 0, data = b'', nonce = None):
        return self._build(private_key, target, value, data, nonce).call()
