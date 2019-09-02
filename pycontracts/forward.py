from eth_utils import keccak
from web3 import Web3

import abc

class Forward(abc.ABC):
    def __init__(self, address):
        self.address = address

    @property
    @abc.abstractmethod
    def owner(self):
        pass

    @abc.abstractmethod
    def nonce(self):
        pass

    def __call__(self, data = b'', target = None, value = 0, nonce = None):
        if hasattr(data, 'buildTransaction'):
            t = data.buildTransaction({"nonce": 0, "gas": 0, "gasPrice": 0})
            data = Web3.toBytes(hexstr = t['data'])
            if not target:
                target = t['to']

        if nonce is None:
            nonce = self.nonce()

        return Call(self, target, value, data, nonce)

    @abc.abstractmethod
    def transact(self, call, originator):
        pass

    @abc.abstractmethod
    def call(self, call, type=bytes):
        pass

class Call:
    def __init__(self, contract, target, value, data, nonce, signature = None):
        self.contract = contract
        self.target = target
        self.value = value
        self.data = data
        self.nonce = nonce
        self.signature = signature

    def signing_data(self):
        return keccak(
            bytes(12) + Web3.toBytes(hexstr=self.contract.address) \
            + self.nonce.to_bytes(32, 'big') \
            + bytes(12) + Web3.toBytes(hexstr=self.target) \
            + self.value.to_bytes(32, 'big') \
            + self.data)

    def sign(self, private_key):
        self.signature = private_key.sign_msg_hash(self.signing_data())
        return self

    def transact(self, originator):
        return self.contract.transact(self, originator)

    def call(self, type=bytes):
        return self.contract.call(self, type)

class CallReverted(Exception):
    def __init__(self, data, call, contract):
        self.data = data
        self.call = call
        self.contract = contract
