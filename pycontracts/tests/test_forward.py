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
    @unittest.skip('not implemented')
    def test_receive_ether(self):
        self.fail()

    @unittest.skip('not implemented')
    def test_send_ether(self):
        self.fail()

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
