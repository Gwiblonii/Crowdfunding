from brownie import Crowdfunding, MockV3Aggregator, accounts, network, exceptions, config, Wei, chain
from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from web3 import Web3
import pytest

def deploy_crowdfunding(goal_usd=100, duration_seconds=60):
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    crowdfunding = Crowdfunding.deploy(
        price_feed_address,
        goal_usd,
        duration_seconds,
        {"from": account}
    )
    return crowdfunding

def test_user_can_request_refund_if_goal_not_met():
    # Arrange
    account = get_account()
    crowdfunding = deploy_crowdfunding(goal_usd=1000, duration_seconds=60)  # meta alta para que no se cumpla
    fund_amount = Wei("0.01 ether")
    # Act: fundear el contrato
    tx = crowdfunding.fund({"from": account, "value": fund_amount})
    tx.wait(1)

    # Simulamos el paso del tiempo
    chain.sleep(61)
    chain.mine(1)


    # Assert: el usuario puede pedir reembolso
    balance_before = account.balance()
    refund_tx = crowdfunding.requestRefund({"from": account})
    refund_tx.wait(1)
    balance_after = account.balance()

    assert balance_after > balance_before - Wei("0.001 ether")

def test_user_cannot_refund_if_not_funded():
    account = get_account()
    crowdfunding = deploy_crowdfunding(goal_usd=1000, duration_seconds=60)

    # Simular paso del tiempo
    chain.sleep(61)
    chain.mine(1)


    # Assert: el usuario que no ha fundeado no puede pedir reembolso
    with pytest.raises(exceptions.VirtualMachineError):
        crowdfunding.requestRefund({"from": account})
