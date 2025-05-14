from brownie import network, config, accounts, MockV3Aggregator

# Configuración del mock del price feed
DECIMALS = 8  # Chainlink devuelve precios con 8 decimales
STARTING_PRICE = 2000 * 10**8  # 2000 USD con 8 decimales

# Redes locales y forkeadas
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]

def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def deploy_mocks():
    print(f"Active network: {network.show_active()}")
    print("Deploying mock price feed...")
    if len(MockV3Aggregator) == 0:  # Evita duplicar mocks si ya existen
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    print("Mocks deployed.")
