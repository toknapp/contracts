import os

from pycontracts.tests.test_settings import faucets, w3, address
from eth_keys import keys

def private_key(balance = None):
    pk = keys.PrivateKey(os.urandom(32))

    if balance:
        tx = w3.eth.sendTransaction(
            {
                "from": faucets.random(),
                "to": address(pk),
                "value": balance
            }
        )
        w3.eth.waitForTransactionReceipt(tx)

    return pk
