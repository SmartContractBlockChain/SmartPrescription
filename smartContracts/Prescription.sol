pragma solidity >=0.7.0;

contract smartPrescription {
    // usually prescription is made by doctor, but here we will stick to general term of prescription creator
    // The keyword public automatically generates a function that allows you to access the current value of
    // the state variable from outside of the contract.
    address public creator;

    struct Drug {
        string name;
        string strength;
        string formulation;
    }

    struct Prescription {
        address patient_address; // Can have all necessary information about patient from his address
        Drug drug;
        string directions;
        string quantity; //No Floats in solidity, should we switch to int ?
        address signature; //Can be used to find name and address of prescriber
        string date;
    }

    Prescription prescription;

    Drug drug;

    address patient;

    // lets assume pharmacist will be visible as well
    address public pharmacist;

    // to indicate wheather prescription was used
    bool public isUsed;

    constructor(
        address _patient_address,
        string memory _directions,
        string memory _quantity,
        string memory _date,
        string memory _name,
        string memory _strength,
        string memory _formulation
    ) {
        creator = msg.sender;
        drug = Drug(_name, _strength, _formulation);
        prescription = Prescription(
            _patient_address,
            drug,
            _directions,
            _quantity,
            creator,
            _date
        );
        patient = _patient_address;
        isUsed = false;

        // here we wont initialize address of pharmacist,
        // as it can be only done when patient will be going to use its prescription
    }

    function setPharmacist(address _pharmacist) public {
        //Should set pharmacist before patient can retrieve his prescription, done by patient
        //this way no one else than the patient can retrieve the prescription
        pharmacist = _pharmacist;
    }

    function getPrescription()
        public
        view
        returns (
            address,
            string memory,
            string memory,
            string memory,
            string memory,
            string memory,
            string memory,
            bool
        )
    {
        return (
            prescription.patient_address,
            prescription.directions,
            prescription.quantity,
            prescription.date,
            drug.name,
            drug.strength,
            drug.formulation,
            isUsed
        );
    }

    function redeem() public returns (bool) {
        require(isUsed == false);
        isUsed = true;
        return (isUsed);
    }
}
