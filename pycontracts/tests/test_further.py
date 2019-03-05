import unittest

from pycontracts.tests.test_settings import *

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.contract = deploy(contracts['further'])

    def test_deploy(self):
        self.assertGreater(len(w3.eth.getCode(self.contract.address)), 1)

    def test_call(self):
        res = w3.eth.call({
            'to': self.contract.address,
        })
        self.assertEqual(int.from_bytes(res, 'big'), 42)
