from scripts.helper import get_account, get_contract, fund_with_link
from brownie import Lottery, network, config
import time


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,  # pricefeed
        get_contract("vrf_coordinator").address,  # vrf coordinator
        get_contract("link_token").address,  # vrf coordinator
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account, "priority_fee": 35000000000},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )

    print("\n----Deployed Lottery!----\n")

    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("\n----Lottery Started!----\n")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 10**8
    enter_tx = lottery.enter({"from": account, "value": value})
    enter_tx.wait(1)
    print("\n----Entered Lottery----\n")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # before ending the contract, fund contract with link token
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_tx = lottery.endLottery({"from": account})
    ending_tx.wait(1)

    # when endLottery() is called chainlink node will respond to fulfillRandomness() and
    # so we will have to wait until fulfillRandomness() goes through
    time.sleep(60)
    print("\n----End Lottery----\n")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
