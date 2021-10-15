//SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

//Brownie can't install npm packages so to use these imports we make some changes in our brownie-config.yaml
//this change tells brownie to install these dependencies from github instead of npm
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
//this gets it from the chainlink npm package
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

// A contract that can accept payment
contract FundMe {
    using SafeMathChainlink for uint256; //This uses SafeMathChainlink for our uint256 operations to prevent overflowing

    // a mapping of new addresses and values sent with it
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders; //creates an array that keeps track of the addresses of funders
    address public owner;
    AggregatorV3Interface public priceFeed;

    //a constructor is called the instant we deploy a smart contract
    // in this case we want it to set the owner to the sender which is the contract admin
    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function fund() public payable {
        //payable is used to specify that a function can accept payments
        uint256 minimumUSD = 50 * 10**18; //This convert 50 dollars to wei by multiplying it with 10 ** 18
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "You need to spend more ETH!"
        );
        addressToAmountFunded[msg.sender] += msg.value; //msg.sender reps the address of the sender and msg.value reps the value of Eth sent with it
        // Adding an external system to know conversion rate
        // what is the ETH -> USD conversion rate
        funders.push(msg.sender);
    }

    //Below we make a call from our contract to an external contract with chainlink and get the version number of the Aggregator Interface
    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData(); //these are the values returned from latestRoundData which is gotten from the AggregatorV3Interface import
        return uint256(answer * 10000000000);
    }

    //
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000; //we divide it by 10^18 to get the correct price
        return ethAmountInUsd;
    }

    function getEntranceFee() public view returns (uint256) {
        //minimum USD
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }

    modifier onlyOwner() {
        //modifiers work like decorators in python
        // set's the contract admin as the owner
        require(msg.sender == owner);
        _; //This tells the contract to run the code below after the _;. It can also be put above the require statement depending on the results needed
    }

    //withdraws all the money that has been funded. Only the admin can do this
    function withdraw() public payable onlyOwner {
        //Here the modifier onlyOwner is run at the beginning of the function. If you want to make it run at the end of the function you can change the position of the _; to the top so it runs the function 1st before the modifier
        msg.sender.transfer(address(this).balance);

        // Below we reset all the funders after we have withdrawn all the money
        //for loop syntax is similar to a js for loop it contains the index, maxvalue and the nextstep (++ or --)
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0); //resets the array
    }
}
// 0x071431E8e44Bbc0d2ab8Eb63FD81CC4d818a65B0
// 0x071431E8e44Bbc0d2ab8Eb63FD81CC4d818a65B0
