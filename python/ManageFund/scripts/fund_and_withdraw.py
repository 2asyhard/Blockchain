from brownie import ManageFund
from scripts.helper import get_account


def fund():
    print("This is fund function")
    manage_fund = ManageFund[-1]
    account = get_account()
    entrance_fee = manage_fund.getEntranceFee()
    print(f"Entrance Fee: {entrance_fee}")
    manage_fund.fund({"from": account, "value": entrance_fee})


def withdraw():
    print("This is withdraw function")
    manage_fund = ManageFund[-1]
    account = get_account()
    manage_fund.withdraw({"from": account})


def main():
    fund()
    withdraw()
