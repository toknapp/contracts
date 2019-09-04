import unittest

import eth_abi

from pycontracts.tests.test_settings import *
from pycontracts.tests import fresh
from pycontracts.forward import CallReverted

class BasicTests:
    def test_deploy(self):
        self.assertGreater(len(w3.eth.getCode(self.fwd.address)), 1)

    def test_owner(self):
        self.assertEqual(self.fwd.owner, address(self.pk))

    def test_owner(self):
        self.assertEqual(self.fwd.owner, address(self.pk))

    def test_nonce(self):
        self.assertEqual(self.fwd.nonce(), 0)

    def test_return_value(self):
        mock = deploy(contracts['Mock'])
        i = random.randint(0, 1000)
        self.assertEqual(self.fwd(mock.functions.echo(i)).sign(self.pk).call(int), i)

    def test_revert(self):
        mock = deploy(contracts['Mock'])
        s = fresh.string()
        with self.assertRaises(CallReverted) as e:
            self.fwd(mock.functions.maybe_fail(s)).sign(self.pk).call()

        self.assertEqual(str(e.exception.data, "UTF-8"), s)

    def test_reentrancy(self):
        mock = deploy(contracts['Mock'])
        i = random.randint(0, 1000)

        n = self.fwd.nonce()
        inner = self.fwd(mock.functions.echo(i), nonce=n+1).sign(self.pk).build()
        bs = self.fwd(inner, nonce=n, target=self.fwd.address).sign(self.pk).call()
        b, bs = eth_abi.decode_single("(bool,bytes)", bs)
        self.assertTrue(b)
        self.assertEqual(i, int.from_bytes(bs, "big"))

class UseCaseTests:
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
        self.fwd(
            target = beneficiary,
            value = v,
        ).sign(self.pk).transact(faucets.random())

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
        self.fwd(contract.functions.set(i)).sign(self.pk).transact(f)

        self.assertEqual(contract.functions.fetch(self.fwd.address).call(), i)

        self.assertEqual(self.fwd(contract.functions.fetch()).sign(self.pk).call(int), i)

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

        # send all tokens
        self.fwd(contract.functions.transfer(beneficiary, v)).sign(self.pk).transact(faucets.random())

        # check the final balances
        self.assertEqual(contract.functions.balanceOf(self.fwd.address).call(), 0)
        self.assertEqual(contract.functions.balanceOf(beneficiary).call(), v)


class SecurityTests:
    def test_reject_incorrect_private_key(self):
        v = random.randint(1, 1000000000)
        faucets.ether(self.fwd.address, v)
        beneficiary = fresh.address()

        # check the initial balances
        self.assertEqual(w3.eth.getBalance(self.fwd.address), v)
        self.assertEqual(w3.eth.getBalance(beneficiary), 0)

        # try calling the contract with an incorrect private key
        with self.assertRaises(ValueError):
            self.fwd(
                target = beneficiary,
                value = v,
            ).sign(fresh.private_key()).transact(faucets.random())

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
            self.fwd(
                target = beneficiary,
                value = v,
                nonce = nonce,
            ).sign(self.pk).transact(faucets.random())

        # check the final balances
        self.assertEqual(w3.eth.getBalance(self.fwd.address), v)
        self.assertEqual(w3.eth.getBalance(beneficiary), 0)

    def test_reject_replay_to_same_contract(self):
        v = random.randint(1, 1000000000)
        faucets.ether(self.fwd.address, v+v)
        beneficiary = fresh.address()

        # check the initial balances
        self.assertEqual(w3.eth.getBalance(self.fwd.address), v+v)
        self.assertEqual(w3.eth.getBalance(beneficiary), 0)

        # make a successful transaction
        tx = self.fwd(
            target = beneficiary,
            value = v,
        ).sign(self.pk).transact(faucets.random())

        # check the intermediate balances
        self.assertEqual(w3.eth.getBalance(self.fwd.address), v)
        self.assertEqual(w3.eth.getBalance(beneficiary), v)

        # try sending the same input in another call
        with self.assertRaises(ValueError):
            w3.eth.sendTransaction({
                "from": faucets.random(),
                "to": self.fwd.address,
                "data": w3.eth.getTransaction(tx).input
            })

        # check the final balances
        self.assertEqual(w3.eth.getBalance(self.fwd.address), v)
        self.assertEqual(w3.eth.getBalance(beneficiary), v)

    def test_reject_incorrect_contract_address(self):
        v = random.randint(1, 1000000000)
        faucets.ether(self.fwd.address, v)
        beneficiary = fresh.address()

        # check the initial balances
        self.assertEqual(w3.eth.getBalance(self.fwd.address), v)
        self.assertEqual(w3.eth.getBalance(beneficiary), 0)

        # make a successful transaction
        tx = self.fwd(
            target = beneficiary,
            value = v,
        ).sign(self.pk).transact(faucets.random())

        # check the intermediate balances
        self.assertEqual(w3.eth.getBalance(self.fwd.address), 0)
        self.assertEqual(w3.eth.getBalance(beneficiary), v)

        # deploy another contract with the same owner and same balance
        other = self.deploy(address(self.pk))
        faucets.ether(other.address, v)

        # try sending the same input in another call to the new contract
        with self.assertRaises(ValueError):
            w3.eth.sendTransaction({
                "from": faucets.random(),
                "to": other.address,
                "data": w3.eth.getTransaction(tx).input
            })

        # check the final balances
        self.assertEqual(w3.eth.getBalance(self.fwd.address), 0)
        self.assertEqual(w3.eth.getBalance(other.address), v)
        self.assertEqual(w3.eth.getBalance(beneficiary), v)

    def test_reject_incorrect_target(self):
        value = random.randint(1, 1000000000)
        faucets.ether(self.fwd.address, value)
        beneficiary = fresh.address()

        # check the initial balances
        self.assertEqual(w3.eth.getBalance(self.fwd.address), value)
        self.assertEqual(w3.eth.getBalance(beneficiary), 0)

        # sign a successful transaction
        f = self.fwd(
            target = beneficiary,
            value = value,
            data = b'',
            nonce = None,
        ).sign(self.pk)

        f.target = fresh.address()
        with self.assertRaises(ValueError):
            self.fwd.transact(f, originator = faucets.random())

        self.assertEqual(w3.eth.getBalance(f.target), 0)
        self.assertEqual(w3.eth.getBalance(beneficiary), 0)
        self.assertEqual(w3.eth.getBalance(self.fwd.address), value)

    def test_reject_incorrect_value(self):
        value = random.randint(1, 1000000000)
        faucets.ether(self.fwd.address, value)
        beneficiary = fresh.address()

        # check the initial balances
        self.assertEqual(w3.eth.getBalance(self.fwd.address), value)
        self.assertEqual(w3.eth.getBalance(beneficiary), 0)

        # sign a successful transaction
        f = self.fwd(
            target = beneficiary,
            value = value,
            data = b'',
            nonce = None,
        ).sign(self.pk)

        f.value = random.randint(1, value - 1)

        with self.assertRaises(ValueError):
            self.fwd.transact(f, originator = faucets.random())

        self.assertEqual(w3.eth.getBalance(beneficiary), 0)
        self.assertEqual(w3.eth.getBalance(self.fwd.address), value)

    def test_reject_incorrect_data(self):
        value = random.randint(1, 1000000000)
        faucets.ether(self.fwd.address, value)
        beneficiary = fresh.address()

        # check the initial balances
        self.assertEqual(w3.eth.getBalance(self.fwd.address), value)
        self.assertEqual(w3.eth.getBalance(beneficiary), 0)

        # sign a successful transaction
        f = self.fwd(
            target = beneficiary,
            value = value,
            data = os.urandom(10),
            nonce = None,
        ).sign(self.pk)

        f.data = os.urandom(10)

        with self.assertRaises(ValueError):
            self.fwd.transact(f, originator = faucets.random())

        self.assertEqual(w3.eth.getBalance(beneficiary), 0)
        self.assertEqual(w3.eth.getBalance(self.fwd.address), value)
