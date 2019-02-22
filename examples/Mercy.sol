pragma solidity ^0.4.0;

library Mercy {
    function mercy(uint amount,uint conversionRate) public pure returns (uint convertedAmount)
	{
		return amount * conversionRate;
	}
}
