from brownie import accounts
from brownie import config  # Set address and private keys
from brownie import StoreData  # Importing contract
from brownie import network

"""         Advantages of using brownie
1. Compile solidity                       -> automatically done by brownie
2. Dump .json file                        -> automatically done by brownie
3. Get byte code and ABI                  -> automatically done by brownie
4. Add local blockchain to use            -> automatically done by brownie
5. Set address and private key            -> your job
"""


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_StoreData():
    """When using local net
    One of `--accounts 10` when execute `brownie compile` in terminal
    account = accounts[0]
    print(account)
    """
    """         When using test net 1
    Manage key everytime run script
        One of safest way to manage private key and highly recommended
    
        1. Add account
            Execute `brownie accounts new <your account>`
            and add private key from your metamask account
            Check for account by executing `brownie accounts list`

        2. Import account
            Execute `accounts.load("<your account>")
            Input password
        
        3. Remove account
            Execute `brownie accounts delete <your account>`
    """
    """         When using test net 2
    Manage key using env variables
        Less secure but you don't have to input password everytime you run script
        
        1. Create .env file
        2. Type in `export PRIVATE_KEY= <0x> + <your private key> in .env file
        3. Create brownie-config.yaml

        4. Type in `dotenv: .env` in brownie-config.yaml file
            Get account by using os
            account = accounts.add(os.getenv("PRIVATE_KEY"))

        5. Add wallets - from_key: ${PRIVATE_KEY"} to brownie-config.yaml
            Get account by using config
            account = accounts.add(config["wallets"]["from_key"])
    """
    account = get_account()  # get account

    store_data = StoreData.deploy({"from": account})  # deploy contract
    # {"from": account} -> Who that I'll be deploying from, or what's the account of deploying this
    # Brownie can distinguish between make transaction or call

    ### Testing
    stored_value = store_data.retrieve()  # make call, so account is unnecessary
    print(stored_value)  # nothings been stored, so value should be 0

    transaction = store_data.store(15)  # make transaction, account is necessary
    transaction.wait(1)  # wait until transaction goes through

    new_stored_value = store_data.retrieve()  # get new stored value
    print(new_stored_value)  # 15 is stored

    """         Testing
    You can code testing functions in smart contract
    But it is more efficient to test in smart contract development framework languages(python, javascript, ...)
    Use tests folder for testing
    """


def main():
    deploy_StoreData()
