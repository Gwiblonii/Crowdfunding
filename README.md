# 🟢 Crowdfunding Smart Contract with Brownie

This project is a crowdfunding smart contract based on Chainlink's [FundMe](https://github.com/PatrickAlphaC/hardhat-fund-me-fcc), built and deployed using [Brownie](https://eth-brownie.readthedocs.io/en/stable/), with unit tests and full functionality deployed on the Sepolia testnet.

## 📌 Project Description

This contract allows users to fund a campaign in ETH. If the campaign reaches its USD goal (using Chainlink Price Feeds) before the deadline, the campaign owner can withdraw the funds. If **the goal is not met**, users can **manually request a refund** of their contributions.

---

## 🛠️ Technologies Used

- Solidity
- Python
- Brownie
- Chainlink Price Feeds
- Ganache CLI
- pytest
- Web3.py
- Sepolia Testnet
- dotenv

---

## 📁 Project Structure

Crowdfunding/
│
├── contracts/
│ ├── Crowdfunding.sol # Main smart contract
│ └── MockV3Aggregator.sol # Mock Chainlink Price Feed
│
├── scripts/
│ ├── deploy.py # Deployment script
│ ├── fund.py # Script to fund the contract
│ ├── withdraw.py # Script to withdraw funds (if goal met)
│ ├── request_refund.py # Script to request refunds
│ ├── verify_contract.py # Contract verification script
│ └── helpful_scripts.py # Utility functions and helpers
│
├── tests/
│ └── test_crowdfunding.py # Automated tests
│
├── .env # Environment variables (ignored)
├── brownie-config.yaml # Brownie configuration
├── .gitignore # Ignore sensitive and temporary files
└── README.md # Project documentation

## 💡 Key Features

-  Fund campaigns with ETH
-  Convert ETH to USD using Chainlink oracles
-  Campaign deadline enforced
-  Manual refund requests if the funding goal is not reached
-  Owner withdrawal if goal is met
-  Contract verification on Etherscan

 ## 🧪 Included Tests
-  Funding test  
-  Successful refund if goal is not met  
-  Refund denied if user has not contributed  

Tests are located in `tests/test_crowdfunding.py`

## 🔐 Security
Require statement checks for:  
- Goal met before allowing withdrawal  
- Campaign ended before allowing refund  
- Owner verification before permitting withdrawals  
- Use of local mocks for unit testing without internet connection

## ✅ Project Status
- 🟢 Completed and fully functional  
- ✔️ Deployed and tested on local network and Sepolia


📄 License
This project is licensed under the MIT License. Feel free to use, modify, and share.

✨ Autor Gwiblonii (Ada)✨
