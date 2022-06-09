// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase, Ownable {

    address payable[] public players;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    uint256 public fee;
    bytes32 public keyhash;
    address payable public recentWinner;
    uint256 public randomness;
    event RequestedRandomness(bytes32 requestId);

    enum LOTTERY_STATE {
        OPEN, 
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;

    constructor(address _priceFeedAddress, address _vrfCoordinator, address _link, uint256 _fee, bytes32 _keyhash) 
    public VRFConsumerBase(_vrfCoordinator, _link) {
        usdEntryFee = 50*(10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        // == lottery_state = 1;
        fee = _fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        // keep track of all the players
        // min $50 entrance fee
        require(lottery_state == LOTTERY_STATE.OPEN);
        require(msg.value >= getEntranceFee(), "Not enough ETH!");
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns(uint256) {
        // check if entrance fee is over 50$
        (,int256 price,,,) = ethUsdPriceFeed.latestRoundData();
        // if entrance fee: 50$, usd/eth: 2000$/1eth
        // 50$ / (2000$/1eth) = 1/40 eth, but solidity doesn't deal with decimals
        // 50 * 100000(bignumber) / 2000

        // change dtype and since pricefeed has 8 decimals, multiply 10**10
        uint256 adjustedPrice = uint256(price) * 10**10;

        uint256 costToEnter = (usdEntryFee*(10**18)) / adjustedPrice;

        return costToEnter;
    }
        
    function startLottery() onlyOwner public {
        require(lottery_state == LOTTERY_STATE.CLOSED, "Can't start new lottery yet");
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public {
        // choose random winner
        // to get true random number use chainlink vrf(verifiable randommness function)
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyhash, fee);

        // when endLottery() is called, contract will request to chainlink node, and
        // the node will respond to fulfillRandomness()
        emit RequestedRandomness(requestId);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness) internal override {
        require(lottery_state == LOTTERY_STATE.CALCULATING_WINNER, "You aren't there yet");
        require(_randomness>0, "random not found");
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];
        recentWinner.transfer(address(this).balance);

        // reset
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }

    
}