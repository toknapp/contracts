import unittest

from pycontracts.forward import ForwardSolidity
from pycontracts.tests import test_forward, fresh
from pycontracts.tests.test_settings import *

class ForwardSolidityTests(
        unittest.TestCase,
        test_forward.BasicTests,
        test_forward.UseCaseTests,
        test_forward.SecurityTests):

    def deploy(self, owner):
        return ForwardSolidity.deploy(w3, owner, originator = faucets.random())

    def setUp(self):
        self.pk = fresh.private_key()
        self.fwd = self.deploy(address(self.pk))
