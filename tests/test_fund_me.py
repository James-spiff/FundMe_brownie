from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import network, accounts, exceptions
from scripts.deploy import deploy_fund_me
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    transaction = fund_me.fund({"from": account, "value": entrance_fee})
    transaction.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    transaction2 = fund_me.withdraw({"from": account})
    transaction2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0

    # addressToAmountFunded is a dictionary we created in the FundMe smart contract that has the address as it's key and amount associated with it as it's value


# a test that makes sure only the owner of the smart contract can withdraw
def test_only_owner_can_withdraw():
    # skips this test if we aren't on a local network
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    # account = get_account()
    fund_me = deploy_fund_me()
    not_owner = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError): #this passes the test if access is denied to a user that doesn't own the smart contract
        fund_me.withdraw({"from": not_owner})