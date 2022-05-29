// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;


contract StoreData {
    uint256 InputNumber;

    struct People {
        uint256 InputNumber;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToInputNumber;

    function store(uint256 _InputNumber) public {
        InputNumber = _InputNumber;
    }

    function retrieve() public view returns (uint256) {
        return InputNumber;
    }

    function addPerson(string memory _name, uint256 _InputNumber) public {
        people.push(People(_InputNumber, _name));
        nameToInputNumber[_name] = _InputNumber;
    }
}