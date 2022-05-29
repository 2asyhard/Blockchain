"""
Read values from contracts that is already deployed

brownie shell that can interact with contracts
    Execute `brownie console`
    It will jump into console that has all the contracts are imported
"""

from brownie import StoreData, accounts, config


def read_contract():
    # read contract from build/deployments/4/0x0ca7~~ (4 is id of rinkeby)
    store_data = StoreData[-1]

    # in order to get deployed contracts, ABI and address is needed
    # brownie already knows the address of the contracts that is saved locally
    # brownie also knows the ABI through .json file in /contracts/ directory

    print(store_data.retrieve())  # 15 should be printed


def main():
    read_contract()
