#!/usr/bin/env python3

import unittest
import random

from test_settings import faucets, w3, deploy, contracts
import fresh

class BasicSanityChecks(unittest.TestCase):
    def test_blockNumber(self):
        w3.eth.blockNumber

    def test_faucets(self):
        for f in faucets.addresses:
            b = w3.eth.getBalance(f)
            self.assertGreater(b, 0)

    def test_faucets_present_in_rpc(self):
        for i, f in enumerate(faucets.addresses):
            self.assertEqual(f, w3.eth.accounts[i])

    def test_fresh_private_key(self):
        pk = fresh.private_key()
        b = w3.eth.getBalance(pk.public_key.to_checksum_address())
        self.assertEqual(b, 0)

    def test_fresh_private_key_with_balance(self):
        w = w3.toWei(random.randint(1, 1000), 'gwei')
        pk = fresh.private_key(balance = w)
        b = w3.eth.getBalance(pk.public_key.to_checksum_address())
        self.assertEqual(b, w)

class ContractSanityChecks(unittest.TestCase):
    def test_echo_call(self):
        contract = deploy(contracts['Echo'])
        i = random.randint(0, 1000)
        self.assertEqual(contract.functions.echo(i).call(), i)

    def test_state_transact(self):
        contract = deploy(contracts['State'])
        i = random.randint(0, 1000)
        tx = contract.functions.set(i).transact({'from': faucets.random()})
        w3.eth.waitForTransactionReceipt(tx)
        self.assertEqual(contract.get_function_by_signature('get()')().call(), i)

class ERC20SanityChecks(unittest.TestCase):
    def test_deployment(self):
        f = faucets.random()
        contract = deploy(contracts['Coin'], faucet = f)
        b = contract.functions.balanceOf(f).call()
        tb = contract.functions.totalSupply().call()
        self.assertEqual(b, tb)

if __name__ == '__main__':
    unittest.main()
