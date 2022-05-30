// SPDX-License-Identifier: MIT

// Smart contract that lets anyone deposit ETH into the contract
// Only the owner of the contract can withdraw the ETH
pragma solidity ^0.6.6;

// Get the latest ETH/USD price from chainlink price feed
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract ManageFund {
    using SafeMathChainlink for uint256; // safe math library check uint256 for integer overflows

    mapping(address => uint256) public addressToAmountFunded; //mapping to store which address depositeded how much ETH
    address[] public funders; // array of addresses who deposited
    address public owner; //address of the owner who deployed the contract
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender; // the first person to deploy the contract is the owner
    }

    function fund() public payable {
        uint256 minimumUSD = 50 * 10**18; // 18 digit number to be compared with donated amount

        require(
            getConversionRate(msg.value) >= minimumUSD, // check if donated fund is less than 50USD?
            "Insufficient ETH!"
        );

        //if not, add to mapping and funders array
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        //function to get the version of the chainlink pricefeed
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        // ETH/USD rate in 18 digit
        return uint256(answer * 10000000000);
    }

    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        // the actual ETH/USD conversation rate, after adjusting the extra 0s.
        return ethAmountInUsd;
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 10**18;
        return (minimumUSD * precision) / price;
    }

    modifier onlyOwner() {
        require(msg.sender == owner); //the message sender must be owner of the contract
        _;
    }

    // check if it's owner, and execute the function
    function withdraw() public payable onlyOwner {
        // If you are using version eight (v0.8) of chainlink aggregator interface, change the code to below
        // payable(msg.sender).transfer(address(this).balance);
        msg.sender.transfer(address(this).balance);

        //iterate through all the mappings and make them 0
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        //reset funders array
        funders = new address[](0);
    }
}
