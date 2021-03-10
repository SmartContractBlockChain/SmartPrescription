pragma solidity >=0.7.0;


contract Prescription {

    // usually prescription is made by doctor, but here we will stick to general term of prescription creator
    // The keyword public automatically generates a function that allows you to access the current value of
    // the state variable from outside of the contract.
    address public creator;

    // for now lets say we will store only medicine name,
    // but this should be some struct - https://docs.soliditylang.org/en/v0.8.1/types.html#structs
    string public medicineName;

    // lets say patient address is not accessible for others
    address patient;

    // lets assume pharmacist will be visible as well
    address public pharmacist;

    // to indicate wheather prescription was used
    bool public isUsed;

    constructor() {
        creator = msg.sender;
        medicineName='_medicine_name';
//        patient=_patient;
        isUsed=false;
        // here we wont initialize address of pharmacist,
        // as it can be only done when patient will be going to use its prescription
    }


    // update after meeting - calling this function need to be done by pharmacist
    //so please go ahead and modify this function
    function reedem(address _pharmacist) public{
        // here we should add more validation to avoid calling this method more than one,
        // sth like require(isUsed=false) plus only the pharmacist should call it so require(msg.sender=pharmacist)
        // should be added

        pharmacist = _pharmacist;
        isUsed = true;
    }
}
