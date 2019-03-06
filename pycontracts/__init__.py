import os
from glob import glob
from binascii import unhexlify

contracts = {}
for contract in glob(os.path.join(os.getenv("CONTRACT_BUILD_PATH"), "[!.]*.bin")):
    name = os.path.basename(contract)[:-4]
    with open(contract, "rb") as h:
        contracts[name] = { 'deploy': unhexlify(h.read()) }

    abi = contract[:-4] + ".abi"
    if os.path.isfile(abi):
        with open(abi, "r") as h:
            contracts[name]['abi'] = h.read()

    init = contract[:-4] + ".init.bin"
    if os.path.isfile(init):
        with open(init, "r") as h:
            contracts[name]['init'] = unhexlify(h.read())

    runtime = contract[:-4] + ".runtime.bin"
    if os.path.isfile(runtime):
        with open(runtime, "r") as h:
            contracts[name]['runtime'] = unhexlify(h.read())
