from brownie import (
    FundMe,
    accounts,
    network,
    config,
    MockV3Aggregator,
)
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    # pass the priceFeed address to our FundMe contract as the 1st parameter
    # Note: if we are on a persistent network like rinkeby use the address otherwise, deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]  # we store our price feed address into our config file so we can easily access different price feeds from different networks by just setting it up in our config and changing the flag here
    else:  # else we use a mock
        deploy_mocks()

        price_feed_address = MockV3Aggregator[
            -1
        ].address  # get's the most recently deployed address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get(
            "verify"
        ),  # get's a value of true or false depending on if we are working on a development network or a live network from the config file
    )  # publish_source=True let's us verify our contract before we can use it we need to create an api key by signing up on ether scan
    print(f"Contract deployed to {fund_me.address}")
    return fund_me  # this is returned so we can easily make use of it in our tests instead of repeating code


def main():
    deploy_fund_me()
