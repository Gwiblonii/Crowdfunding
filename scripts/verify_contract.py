from brownie import Crowdfunding, config, network

def main():
    crowdfunding = Crowdfunding[-1]
    Crowdfunding.publish_source(crowdfunding)
