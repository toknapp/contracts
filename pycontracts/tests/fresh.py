import os
import random

from string import ascii_uppercase, digits

from pycontracts.tests.test_settings import faucets, w3, address as to_address
from eth_keys import keys

def private_key(balance = None):
    pk = keys.PrivateKey(os.urandom(32))
    if balance: faucets.ether(to_address(pk), balance)
    return pk

def address():
    return to_address(private_key())

def string(N=12, alphabeth=ascii_uppercase+digits):
    return ''.join(random.choice(alphabeth) for _ in range(N))
