import unittest

from pycontracts import forward
from pycontracts.tests.test_settings import *
from pycontracts.tests import fresh

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.pk = fresh.private_key()
        self.fwd = forward.deploy(
            w3,
            owner = address(self.pk),
            originator = faucets.random()
        )

    def test_deploy(self):
        self.assertGreater(len(w3.eth.getCode(self.fwd.address)), 1)

    def test_owner(self):
        self.assertEqual(self.fwd.owner, address(self.pk))

    def test_nonce(self):
        self.assertEqual(self.fwd.nonce(), 0)

class UseCaseTests(unittest.TestCase):
    def setUp(self):
        self.pk = fresh.private_key()
        self.fwd = forward.deploy(
            w3,
            owner = address(self.pk),
            originator = faucets.random()
        )

    def test_receive_ether(self):
        self.assertEqual(w3.eth.getBalance(self.fwd.address), 0)

        v = random.randint(0, 1000000000)
        faucets.ether(self.fwd.address, v)

        self.assertEqual(w3.eth.getBalance(self.fwd.address), v)

    def test_send_ether(self):
        # provision some eth
        v = random.randint(1, 1000000000)
        faucets.ether(self.fwd.address, v)

        # pick a beneficiary
        beneficiary = fresh.address()

        # check the initial balances
        self.assertEqual(w3.eth.getBalance(self.fwd.address), v)
        self.assertEqual(w3.eth.getBalance(beneficiary), 0)

        # send all ether
        self.fwd.transact(
            private_key = self.pk,
            target = beneficiary,
            value = v,
            originator = faucets.random()
        )

        # check that the nonce got bumped
        self.assertEqual(self.fwd.nonce(), 1)

        # check the final balances
        self.assertEqual(w3.eth.getBalance(self.fwd.address), 0)
        self.assertEqual(w3.eth.getBalance(beneficiary), v)

    def test_simple_contract_interaction(self):
        contract = deploy(contracts['State'])

        i = random.randint(0, 1000)

        self.assertEqual(contract.functions.fetch(self.fwd.address).call(), 0)

        f = faucets.random()
        self.fwd.transact(
            private_key = self.pk,
            data = contract.functions.set(i),
            originator = f
        )

        self.assertEqual(contract.functions.fetch(self.fwd.address).call(), i)
        # TODO: when return values have been implemented:
        # self.assertEqual(self.fwd.call(private_key = self.pk, data = contract.functions.fetch()), i)


    def test_transfer_erc20(self):
        # provision a coin and some tokens
        f = faucets.random()
        contract = deploy(contracts['Coin'], faucet = f)
        v = random.randint(0, 1000)
        contract.functions.transfer(self.fwd.address, v).transact({ 'from': f })

        # pick a beneficiary
        beneficiary = fresh.address()

        # check the initial balances
        self.assertEqual(contract.functions.balanceOf(self.fwd.address).call(), v)
        self.assertEqual(contract.functions.balanceOf(beneficiary).call(), 0)

        # send all ether
        self.fwd.transact(
            private_key = self.pk,
            data = contract.functions.transfer(beneficiary, v),
            originator = faucets.random()
        )

        # check the final balances
        self.assertEqual(contract.functions.balanceOf(self.fwd.address).call(), 0)
        self.assertEqual(contract.functions.balanceOf(beneficiary).call(), v)


    @unittest.skip('not implemented')
    def test_return_value(self):
        self.fail()

class SecurityTests(unittest.TestCase):
    def setUp(self):
        self.pk = fresh.private_key()
        self.fwd = forward.deploy(
            w3,
            owner = address(self.pk),
            originator = faucets.random()
        )

    def test_reject_incorrect_private_key(self):
        v = random.randint(1, 1000000000)
        faucets.ether(self.fwd.address, v)
        beneficiary = fresh.address()

        # check the initial balances
        self.assertEqual(w3.eth.getBalance(self.fwd.address), v)
        self.assertEqual(w3.eth.getBalance(beneficiary), 0)

        # try calling the contract with an incorrect private key
        with self.assertRaises(ValueError):
            self.fwd.transact(
                private_key = fresh.private_key(),
                target = beneficiary,
                value = v,
                originator = faucets.random()
            )

        # check the final balances
        self.assertEqual(w3.eth.getBalance(self.fwd.address), v)
        self.assertEqual(w3.eth.getBalance(beneficiary), 0)

    def test_reject_incorrect_nonce(self):
        v = random.randint(1, 1000000000)
        faucets.ether(self.fwd.address, v)
        beneficiary = fresh.address()

        # check the initial balances
        self.assertEqual(w3.eth.getBalance(self.fwd.address), v)
        self.assertEqual(w3.eth.getBalance(beneficiary), 0)

        # try calling the contract with an incorrect nonce
        correct_nonce = self.fwd.nonce()
        ns = list(filter(lambda i: i != correct_nonce, range(100000)))
        nonce = random.choice(ns)

        with self.assertRaises(ValueError):
            self.fwd.transact(
                private_key = self.pk,
                target = beneficiary,
                value = v,
                originator = faucets.random(),
                nonce = nonce
            )

        # check the final balances
        self.assertEqual(w3.eth.getBalance(self.fwd.address), v)
        self.assertEqual(w3.eth.getBalance(beneficiary), 0)

    @unittest.skip('not implemented')
    def test_reject_incorrect_contract_address(self):
        self.fail()
