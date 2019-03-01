from web3 import Web3, HTTPProvider, TestRPCProvider
from eth_keys import keys

from binascii import unhexlify
from glob import glob
import os

target = os.getenv("GANACHE_TARGET")
w3 = Web3(HTTPProvider(target))

faucets = map(lambda f: unhexlify(f), [
    "e2ee547be17ac9f7777d4763c43fd726c0a2a6d40450c92de942d7925d620b6d",
    "0740fb09781e8fa771edcf1bddee93ad6772593b3139f1cf36b0d095d235887b",
    "ac72e464dac0448a28fa71b34bfe46b2356fe09bd4f5a73519ee60b3b92b9dab",
    "230eda6cc73da415d3b327426dde475a786bb5a0aeae2ca531aaaa8c0218a7a5",
    "91e3179925ef60e4d1f4daf0e7d67bdb5cf74ff3d456db0eb239e432290db31c",
    "66769c67a372926b945262a1c86b7944a669dbeab3d89771d7af691b3bfb20d8",
    "af40a15c4d369cdb39d01148d7b5f5dd4f9825447fabcbfc15e230db84fcb88b",
    "4ad882b7e0b24fd01ad6d2f281d469edb9d2bef2c2ee8871099c5fd7c7018317",
    "9042fc069b6abe8210d31195b382b61c3ee9149223fcb181016a49ba61a14d84",
    "bf32730f2b240c0c482126ecc1e2219554f3c738f19bd592e3ccf4cc005ddc1e",
])

faucet_addresses = map(lambda f: keys.PrivateKey(f).public_key.to_checksum_address(), faucets)

contract_sources = {}
for contract in glob(os.path.join(os.getenv("CONTRACT_BUILD_PATH"), "*.bin")):
    name = os.path.basename(contract)[:-4]
    with open(contract, "rb") as h:
        contract_sources[name] = unhexlify(h.read())
