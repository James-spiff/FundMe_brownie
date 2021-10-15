from brownie import (
    accounts,
    network,
    config,
    MockV3Aggregator,
)  # MockV3Aggregator is a mock file gotten from https://github.com/smartcontractkit/chainlink-mix/blob/master/contracts/test/MockV3Aggregator.sol and saved in the contracts/test folder
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]    #a forked environment is a copy of a live blockchain on a mainnet that runs locally and can be interacted with the same way as a live mainnet blockchain
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

# below are the parameters for the MockV3Aggregator contract
DECIMALS = 8
STARTING_PRICE = 200000000000


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks...")
    if len(MockV3Aggregator) <= 0:  # contracts are returned as lists so we can interact with them in the same way
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})  # Web3.toWei() converts ether to wei
    print("Mocks Deployed!")
