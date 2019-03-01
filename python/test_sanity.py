#!/usr/bin/env python3

import unittest
from test_settings import w3, faucets, faucet_addresses

class SanityCheck(unittest.TestCase):
    def test_blockNumber(self):
        w3.eth.blockNumber

    def test_faucets(self):
        for f in faucet_addresses:
            b = w3.eth.getBalance(f)
            self.assertGreater(b, 0)

    def test_faucets_present_in_rpc(self):
        for i, f in faucet_addresses:
            self.assertEqual(f, w3.eth.accounts[i])

if __name__ == '__main__':
    unittest.main()
