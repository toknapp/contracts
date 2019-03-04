import os

from pycontracts.tests.test_settings import faucets, w3, address as to_address
from eth_keys import keys

def private_key(balance = None):
    pk = keys.PrivateKey(os.urandom(32))

    if balance:
        tx = w3.eth.sendTransaction(
            {
                "from": faucets.random(),
                "to": to_address(pk),
                "value": balance
            }
        )

    return pk

def address():
    return to_address(private_key())
