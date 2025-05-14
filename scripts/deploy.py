from brownie import Crowdfunding, MockV3Aggregator, config, network
from scripts.helpful_scripts import deploy_mocks, get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from web3 import Web3

GOAL_USD = 100  # Meta de 100 USD
DURATION_SECONDS = 7 * 24 * 60 * 60 # 7 días en segundos

def deploy_crowdfunding():
    account = get_account()

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    print(f"Deploying from account: {account}")
    print(f"Balance: {account.balance()}")

    crowdfunding = Crowdfunding.deploy(
        price_feed_address,
        GOAL_USD,
        DURATION_SECONDS,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False)
    )

    print(f"Contract deployed to {crowdfunding.address}")
    return crowdfunding

def main():
    deploy_crowdfunding()