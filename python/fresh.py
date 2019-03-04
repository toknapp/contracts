import os

from test_settings import faucets, w3
from eth_keys import keys

def private_key(balance = None):
    pk = keys.PrivateKey(os.urandom(32))

    if balance:
        tx = w3.eth.sendTransaction(
            {
                "from": faucets.random(),
                "to": pk.public_key.to_checksum_address(),
                "value": balance
            }
        )
        w3.eth.waitForTransactionReceipt(tx)

    return pk
