"""
1. Swap our ETH for WETH
2. Deposit some ETH(WETH) into aave
3. Borrow some asset with the ETH collateral
4. Repay everything back
"""
from scripts.helper import get_account
from brownie import network, config, interface
from scripts.get_weth import get_weth
from web3 import Web3


# 0.1
amount = Web3.toWei(0.1, "ether")


def main():
    # 1. get WETH using ETH
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth()

    # 2. deposit to aave

    # get lending pool contract
    lending_pool = get_lending_pool()

    # approve(needs to be approved by erc20 token function before sending it)
    approve_erc20(amount, lending_pool.address, erc20_address, account)

    # make deposit
    tx = lending_pool.deposit(
        erc20_address,  # address asset
        amount,  # amount to deposit
        account.address,  # my account address
        0,  # deprecated
        {"from": account},
    )
    print("Depositing...")
    tx.wait(1)
    print("Deposited!!!\n")

    # 3. borrow
    # check my status
    available_borrow_eth, total_debt_eth = get_borrowable_data(lending_pool, account)

    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )

    borrow_rate = 0.95  # to take pre-caution of liquidation
    # borrowable eth -> borrowable dai * borrow_rate
    amount_dai_to_borrow = (1 / dai_eth_price) * (available_borrow_eth * borrow_rate)
    print(f"We are going to borrow {amount_dai_to_borrow} DAI")

    # execute borrow function
    dai_address = config["networks"][network.show_active()]["dai_token"]
    # https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool#borrow
    # borrow(address asset, uint256 amount, uint256 interestRateMode, uint16 referralCode, address onBehalfOf)
    borrow_tx = lending_pool.borrow(
        dai_address,
        Web3.toWei(amount_dai_to_borrow, "ether"),
        1,  # 1: stable, 2: variable
        0,
        account.address,
        {"from": account},
    )
    borrow_tx.wait(1)
    print("Successfully borrowed!!")
    get_borrowable_data(lending_pool, account)

    # 4. repay
    repay_all(amount, lending_pool, account)

    print("You just deposited, borrowed and repayed with Aave, Brownie and Chainlink!")


def repay_all(amount, lending_pool, account):
    # approve
    approve_erc20(
        Web3.toWei(amount, "ether"),
        lending_pool,
        config["networks"][network.show_active()]["dai_token"],
        account,
    )
    # https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool#repay
    # repay(address asset, uint256 amount, uint256 rateMode, address onBehalfOf)
    repay_tx = lending_pool.repay(
        config["networks"][network.show_active()]["dai_token"],
        amount,
        1,
        account.address,
        {"from": account},
    )
    repay_tx.wait(1)
    print("Repayed!")


def get_asset_price(price_feed_address):
    dai_eth_price_feed = interface.IAggregatorV3(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    converted_latest_price = Web3.fromWei(latest_price, "ether")
    print(f"The DAI/ETH price: {converted_latest_price} ETH")
    return float(converted_latest_price)


def get_borrowable_data(lending_pool, account):
    """
    get accounts status using getUserAccountData()
    function returns total collateral, total dept, available borrow capacity
    https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool#getuseraccountdata
    it's a view function, doesn't spend any gas

    also see liquidation infos
        https://docs.aave.com/risk/asset-risk/risk-parameters
    """

    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)

    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")

    print(f"You have {total_collateral_eth} worth of ETH deposited")
    print(f"You have {total_debt_eth} worth of ETH borrowed")
    print(f"You can borrow {available_borrow_eth} worth of ETH")

    return float(available_borrow_eth), float(total_debt_eth)


def approve_erc20(amount, spender, erc20_address, account):
    """get interface
    use eip20(https://eips.ethereum.org/EIPS/eip-20)
    IERC20.sol approve function has spender and value input
    and we also need my erc20 token address and account
    """
    print("Approving ERC20 token")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)  # wait 1 block confirmation for finish
    print("Approved")
    return tx


def get_lending_pool():
    """
    lending pool contracts address can change depending on conditions
    so use LendingPoolAddressesProvider to get valid lending pool contracts address
    url: https://docs.aave.com/developers/v/1.0/developing-on-aave/the-protocol/lendingpooladdressesprovider
    """
    """
    if your going to work with 1 or 2 functions in contracts
    you can just make interfaces by yourself
    """

    # get lending pool address by using lending pool address provider
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)

    return lending_pool
