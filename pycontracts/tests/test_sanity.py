#!/usr/bin/env python3

import unittest
import random

from pycontracts.tests.test_settings import *
from pycontracts.tests import fresh
from pycontracts import contracts

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
        b = w3.eth.getBalance(address(pk))
        self.assertEqual(b, 0)

    def test_fresh_private_key_with_balance(self):
        w = w3.toWei(random.randint(1, 1000), 'gwei')
        pk = fresh.private_key(balance = w)
        b = w3.eth.getBalance(address(pk))
        self.assertEqual(b, w)

class ContractSanityChecks(unittest.TestCase):
    def test_echo_call(self):
        contract = deploy(contracts['Mock'])
        i = random.randint(0, 1000)
        self.assertEqual(contract.functions.echo(i).call(), i)

    def test_state_empty(self):
        contract = deploy(contracts['State'])
        self.assertEqual(contract.functions.fetch().call(), 0)
        self.assertEqual(contract.functions.fetch(fresh.address()).call(), 0)

    def test_state_transact(self):
        f = faucets.random()
        contract = deploy(contracts['State'], faucet = f)
        i = random.randint(0, 1000)
        contract.functions.set(i).transact({'from': f})
        self.assertEqual(contract.functions.fetch().call({'from': f}), i)
        self.assertEqual(contract.functions.fetch(f).call(), i)

    def test_mock_fail(self):
        mock = deploy(contracts['Mock'])
        s = fresh.string()

        self.assertEqual(mock.functions.maybe_fail(True, s).call(), s)

        with self.assertRaises(ValueError) as e:
            mock.functions.maybe_fail(False, s).call()
        self.assertEqual(extract_revert_data(e.exception), s)

class ERC20SanityChecks(unittest.TestCase):
    def test_deployment(self):
        f = faucets.random()
        contract = deploy(contracts['Coin'], faucet = f)
        b = contract.functions.balanceOf(f).call()
        tb = contract.functions.totalSupply().call()
        self.assertEqual(b, tb)

    def test_fresh_address_has_no_tokens(self):
        contract = deploy(contracts['Coin'])
        pk = fresh.private_key()
        b = contract.functions.balanceOf(address(pk)).call()
        self.assertEqual(b, 0)

    def test_transfer(self):
        f = faucets.random()
        contract = deploy(contracts['Coin'], faucet = f)
        pk = fresh.private_key()
        v = random.randint(0, 1000)
        contract.functions.transfer(address(pk), v).transact({ 'from': f })
        b = contract.functions.balanceOf(address(pk)).call()
        self.assertEqual(b, v)

if __name__ == '__main__':
    unittest.main()
