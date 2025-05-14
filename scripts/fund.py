from brownie import Crowdfunding, Wei
from scripts.helpful_scripts import get_account
from web3 import Web3

def fund():
    crowdfunding = Crowdfunding[-1]
    account = get_account()
    
    # Queremos enviar al menos el equivalente a 1 USD en ETH
    # Para eso usamos getPrice() que devuelve el precio de 1 ETH en USD con 18 decimales
    eth_price = crowdfunding.getPrice()  # Por ejemplo, 2000 * 1e18

    # 1 USD en ETH sería: 1 * 10**18 / eth_price
    minimum_usd = Wei("1 ether")
    eth_amount = minimum_usd * (10**18) // eth_price + 1  # Le sumamos 1 para asegurar que pase el require

    print(f"Funding with {eth_amount} wei (~1 USD)")
    tx = crowdfunding.fund({"from": account, "value": eth_amount})
    tx.wait(1)
    print("Funded!")

def main():
    fund()
