from brownie import ManageFund, MockV3Aggregator, network, config
from scripts.helper import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENT


def deploy_manage_fund():
    account = get_account()

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        # if network to deploy is persistent like rinkeby, use address from config
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]

    else:
        """
        else deploy mock, because price feed address doesn't exists in local network
        to fix this deploy fake price feed contract using mock
        1. create 'test' directory in contracts/
        2. copy/paste chainlink-mix/test/MockV3Aggregator.sol from github to contracts/test/
        """
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    manage_fund = ManageFund.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
        # when publish_source=True, you can verify your contract code in etherscan
        # you have to add etherscan api key as ETHERSCAN_TOKEN in .env file
    )

    # I executed fund() here instead of scripts.fund_and_withdraw,
    # because I was unable to install ganache in docker container
    # from scripts.fund_and_withdraw import fund, withdraw
    # fund()
    # withdraw()

    print(f"\nContract deployed to {manage_fund.address}\n")

    return manage_fund


def main():
    deploy_manage_fund()


"""
Add networks on brownie
    add ganache local network to Ethereum
        Execute `brownie networks add Ethereum ganache-local host=http://0.0.0.0:8545 chainid=1337`

    add custom network using alchemy.io(https://www.alchemy.com/)
        Execute `brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork='<your HTTP key from personal app of alchemy.io>' accounts=10 mnemonic=brownie port=8545`

    check network list
        Execute `brownie networks list`
"""
