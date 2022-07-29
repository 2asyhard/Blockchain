from scripts.helper import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENT
from scripts.deploy import deploy_manage_fund
from brownie import network, accounts, exceptions, network
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    manage_fund = deploy_manage_fund()
    entrance_fee = manage_fund.getEntranceFee() + 100
    tx = manage_fund.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert manage_fund.addressToAmountFunded(account.address) == entrance_fee
    tx2 = manage_fund.withdraw({"from": account})
    tx2.wait(1)
    assert manage_fund.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        # skip test if your not on local network
        pytest.skip("Only for local test")

    manage_fund = deploy_manage_fund()
    wrong_account = accounts.add()  # this will give blank account
    with pytest.raises(exceptions.VirtualMachineError):
        # if error occur test will pass
        manage_fund.withdraw({"from": wrong_account})
