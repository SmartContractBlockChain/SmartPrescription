pragma solidity >=0.7.0;


contract Prescription {

    // usually prescription is made by doctor, but here we will stick to general term of prescription creator
    // The keyword public automatically generates a function that allows you to access the current value of
    // the state variable from outside of the contract.
    address public creator;

     struct Drug{
        string _name;
        string _strength;
        string _formulation;
    }

    struct Prescription {
        address patient_address; // Can have all necessary information about patient from his address
        Drug drug;
        string directions;
        string quantity; //No Floats in solidity, should we switch to int ?
        address signature; //Can be used to find name and address of prescriber
        string date;
    }

    address patient;

    // lets assume pharmacist will be visible as well
    address public pharmacist;

    // to indicate wheather prescription was used
    bool public isUsed;

    constructor(address _patient_address, string memory _directions, string memory _quantity, string memory _date, string memory _name, string memory _strength, string memory _formulation) {
        creator = msg.sender; // TODO: Make a check that the construction of the prescription can only be done by a doctor with a require from a database of doctors address?
        Drug memory drug = Drug(_name, _strength, _formulation);
        Prescription memory prescription = Prescription(_patient_address, drug, _directions, _quantity, creator, _date);
        patient=_patient_address;
        isUsed=false;
        
        // here we wont initialize address of pharmacist,
        // as it can be only done when patient will be going to use its prescription
    }

    function setPharmacist(address _pharmacist) public {
        //Should set pharmacist before patient can retrieve his prescription, done by patient
        require(msg.sender == patient) //this way no one else than the patient can retrieve the prescription
        pharmacist = _pharmacist;
    }
    

    function reedem(address _patient) public{
        // here we should add more validation to avoid calling this method more than once, anyway to delete the contract once done ?
        require(msg.sender == pharmacist && isUsed==false);
        isUsed = true;
        //TODO: need to display the prescription here when redeeming so pharmacist can atctually do it 
    }
}
