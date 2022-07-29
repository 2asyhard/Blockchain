from brownie import network, accounts, config
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENT = [
    "development",
    "ganache-local",
    "ganache",
    "hardhat",
    "mainnet-fork",
]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        return accounts[0]
    if id:
        return accounts.load(id)
    if network.show_active() in config["networks"]:
        return accounts.add(config["wallets"]["from_key"])
