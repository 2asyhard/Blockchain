from scripts.helper import get_account
from brownie import interface, network, config


def main():
    get_weth()


def get_weth():
    """
    WETH(Wrapped ETH) is one of erc20 token
    mints WETH by depositing ETH
    1. interact with WETHGateway from etherscan
    2. use contract
        etherscan kovan: https://kovan.etherscan.io/token/0xd0a1e359811322d97991e03f863a0c30c2cf029c#writeContract
        use deposit/withdraw functions
    use contract direct from interface directory

    """

    account = get_account()
    # ABI / Address
    # get weth contract
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])

    # call function and deposit 0.1 eth
    tx = weth.deposit({"from": account, "value": 0.1 * 10**18})
    tx.wait(1)
    return tx
