pragma solidity >=0.7.0;

contract smartPrescription {
    // The keyword public automatically generates a function that allows you to access the current value of
    // the state variable from outside of the contract.
    address public creator;

    struct Drug {
        string name;
        string strength;
        string formulation;
    }

    struct Prescription {
        address patient_address; // Unique to a patient
        Drug drug;
        string directions;
        string quantity; //No Floats in solidity, as drugs can have decimal points, use string
        address signature; // Address of the creator of the prescription i.e a doctor
        string date;
    }

    Prescription prescription;

    Drug drug;

    // lets assume pharmacist will be visible as well
    address public pharmacist;

    // to indicate wheather prescription was used
    bool public isUsed;

    bool public patientSignature;

    constructor(
        address _patient_address,
        address _pharmacist_address,
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
        pharmacist = _pharmacist_address;
        isUsed = false;
        patientSignature = false;
    }

    function patientSign() public returns (bool) {
        require(
            patientSignature == false &&
                msg.sender == prescription.patient_address
        );
        patientSignature = true;
        return patientSignature;
    }

    function getPrescription()
        public
        view
        returns (
            address,
            address,
            string memory,
            string memory,
            string memory,
            string memory,
            string memory,
            string memory,
            bool,
            bool
        )
    {
        require(
            msg.sender == pharmacist ||
                msg.sender == prescription.patient_address ||
                msg.sender == creator
        );
        return (
            prescription.patient_address,
            pharmacist,
            prescription.directions,
            prescription.quantity,
            prescription.date,
            drug.name,
            drug.strength,
            drug.formulation,
            isUsed,
            patientSignature
        );
    }

    function redeem() public returns (bool) {
        require(
            isUsed == false &&
                patientSignature == true &&
                msg.sender == pharmacist
        );
        isUsed = true;
        return (isUsed);
    }
}
// TODO: Create a function to add a drug to the prescription
