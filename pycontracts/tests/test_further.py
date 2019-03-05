import unittest

from pycontracts.tests.test_settings import *

class BasicTests(unittest.TestCase):
    def test_deploy(self):
        contract = deploy(contracts['further'])
        self.assertGreater(len(w3.eth.getCode(contract.address)), 1)
