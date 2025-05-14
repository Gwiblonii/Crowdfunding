// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract Crowdfunding {
    // ===================== State Variables =====================
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner;
    uint256 public goal;
    uint256 public deadline;
    AggregatorV3Interface public priceFeed;

    // ===================== Constructor =====================
    constructor(
        address _priceFeed,
        uint256 _goalUSD,
        uint256 _durationSeconds
    ) {
        owner = msg.sender;
        goal = _goalUSD * 10 ** 18; // goal en USD con 18 decimales
        deadline = block.timestamp + _durationSeconds;
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    // ===================== Fund Function =====================
    function fund() public payable {
        require(block.timestamp < deadline, "Campaign has ended");
        uint256 minimumUSD = 1 * 10 ** 18; // Opcional: mínimo de 1 USD para contribuir
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "Need to spend more ETH"
        );

        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    // ===================== Withdraw (solo si la metya se cumple) =====================
    modifier onlyOwner() {
        require(msg.sender == owner, "Not contract owner");
        _;
    }

    function withdrawFunds() public onlyOwner {
        require(block.timestamp >= deadline, "Campaign still active");
        require(getTotalUSD() >= goal, "Goal not reached");
        payable(msg.sender).transfer(address(this).balance);

        // Reset balances
        for (uint256 i = 0; i < funders.length; i++) {
            address funder = funders[i];
            addressToAmountFunded[funder] = 0;
        }
        delete funders; // Aquí está la corrección final
    }

    // ===================== Refund a aportadores (si la meta no se cumple) =====================
    function requestRefund() public {
        require(block.timestamp >= deadline, "Campaign still active");
        require(getTotalUSD() < goal, "Goal was reached");
        uint256 amount = addressToAmountFunded[msg.sender];
        require(amount > 0, "No funds to refund");

        addressToAmountFunded[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }

    // ===================== Chainlink Price Feed (oraculo)=====================
    function getPrice() public view returns (uint256) {
        (, int256 price, , , ) = priceFeed.latestRoundData();
        // ETH/USD tiene 8 decimales, ajustamos a 18
        return uint256(price) * 10 ** 10;
    }

    function getConversionRate(
        uint256 ethAmount
    ) public view returns (uint256) {
        uint256 ethPrice = getPrice(); // en USD con 18 decimales
        return (ethPrice * ethAmount) / 10 ** 18;
    }

    function getTotalUSD() public view returns (uint256) {
        return getConversionRate(address(this).balance);
    }

    // ============= Utils (muestra la lista de aportadores y el temporizador) =====================
    function getFunders() public view returns (address[] memory) {
        return funders;
    }

    function getTimeLeft() public view returns (uint256) {
        if (block.timestamp >= deadline) return 0;
        return deadline - block.timestamp;
    }
}
