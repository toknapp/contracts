from pycontracts import contracts
from pycontracts.forward import Forward, CallReverted
from web3 import Web3
import eth_abi

class Further(Forward):
    def __init__(self, w3, address, owner = None):
        super().__init__(address)
        self.w3 = w3
        self._owner = owner

    @staticmethod
    def wrap(w3, address, owner = None):
        return Further(w3, address, owner)

    @staticmethod
    def deploy(w3, owner, originator):
        def push(bs):
            return (0x60 + len(bs) - 1).to_bytes(1, 'big') + bs

        init = push(Web3.toBytes(hexstr=owner)) + contracts['further']['deploy']

        tx_hash = w3.eth.sendTransaction({
            'from': originator,
            'data': init,
        })
        r = w3.eth.waitForTransactionReceipt(tx_hash)
        return Further.wrap(w3, r.contractAddress, owner)

    @property
    def owner(self):
        if not self._owner:
            bs = self.w3.eth.call({ 'to': self.address })
            self._owner = Web3.toChecksumAddress(Web3.toHex(bs[:20]))
        return self._owner

    def nonce(self):
        bs = self.w3.eth.call({ 'to': self.address })
        return int.from_bytes(bs[20:20+32], 'big')

    @staticmethod
    def build(call):
        return (27 + call.signature.v).to_bytes(1, 'big') \
            + call.signature.r.to_bytes(32, 'big') \
            + call.signature.s.to_bytes(32, 'big') \
            + bytes(12) + Web3.toBytes(hexstr=call.target) \
            + call.value.to_bytes(32, 'big') \
            + call.data

    def transact(self, call, originator):
        return self.w3.eth.sendTransaction({
            'to': self.address,
            'from': originator,
            'data': Further.build(call),
            'gasLimit': 10000000000
        })

    def call(self, call, type=bytes):
        res = self.w3.eth.call({
            'to': self.address,
            'data': Further.build(call),
            'gasLimit': 10000000000,
        })

        success, return_data = eth_abi.decode_single("(bool,bytes)", res)

        if success:
            if type == bytes: return return_data
            elif type == int: return int.from_bytes(return_data, 'big')
            else: raise TypeError(f"unsupported type: {type}")
        else:
            raise CallReverted(return_data, call, self)
