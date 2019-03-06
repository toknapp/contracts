import unittest

from pycontracts.tests.test_settings import *

class BareMetalTests(unittest.TestCase):
    def setUp(self):
        self.contract = deploy(contracts['bare_metal'])
        self.runtime = contracts['bare_metal']['runtime']

    def test_deploy(self):
        self.assertEqual(
            w3.eth.getCode(self.contract.address),
            self.runtime
        )

    def test_call(self):
        res = w3.eth.call({ 'to': self.contract.address, })
        self.assertEqual(int.from_bytes(res, 'big'), 42)
