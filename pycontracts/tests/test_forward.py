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
        tx = w3.eth.sendTransaction({
            "from": faucets.random(),
            "to": self.fwd.address,
            "value": v,
            "gas": 90000,
        })

        self.assertEqual(w3.eth.getBalance(self.fwd.address), v)

    def test_send_ether(self):
        # provision some eth
        v = random.randint(1, 1000000000)
        tx = w3.eth.sendTransaction({
            "from": faucets.random(),
            "to": self.fwd.address,
            "value": v,
        })

        # pick a beneficiary
        beneficiary = address(fresh.private_key())
        self.assertEqual(w3.eth.getBalance(self.fwd.address), v)
        self.assertEqual(w3.eth.getBalance(beneficiary), 0)

        # send all ether
        tx = self.fwd.transact(
            private_key = self.pk,
            target = beneficiary,
            value = v,
            originator = faucets.random()
        )

        # check that the nonce got bumped
        self.assertEqual(self.fwd.nonce(), 1)

        # check the updated balances
        self.assertEqual(w3.eth.getBalance(self.fwd.address), 0)
        self.assertEqual(w3.eth.getBalance(beneficiary), v)

    @unittest.skip('not implemented')
    def test_transfer_erc20(self):
        self.fail()

    @unittest.skip('not implemented')
    def test_return_value(self):
        self.fail()

class SecurityTests(unittest.TestCase):
    @unittest.skip('not implemented')
    def test_reject_invalid_signature(self):
        self.fail()

    @unittest.skip('not implemented')
    def test_reject_incorrect_nonce(self):
        self.fail()

    @unittest.skip('not implemented')
    def test_reject_incorrect_contract_address(self):
        self.fail()
