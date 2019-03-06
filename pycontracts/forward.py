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

    def signing_data(self, target, value, data, nonce):
        return keccak(
            bytes(12) + Web3.toBytes(hexstr=self.address) \
            + bytes(12) + Web3.toBytes(hexstr=target) \
            + value.to_bytes(32, 'big') \
            + nonce.to_bytes(32, 'big') \
            + data)

    @abc.abstractmethod
    def sign(self, private_key, target, value, data, nonce):
        pass

    @abc.abstractmethod
    def transact(self, private_key, originator, target = None, value = 0, data = b'', nonce = None):
        pass
