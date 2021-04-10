pragma solidity >=0.7.0;

contract smartPrescription {

    struct Drug {
        string name;
        string strength;
        string formulation;
    }

     // address of doctor
    address public creator;
    address patient_address;
    Drug drug;
    string directions;
    string quantity;
    string date;

    //all pharmacist where patient can reedem the prescription
    address[] public pharmacists;

    bool public isUsed;

    bool public isPatientSigned;
    // address of pharmacist where patient can redeemed the prescription
    address prescriptionRedeemedAt;

    mapping (address => bool) private pharmacist_address_map;

    function setPharmacists(address[] memory _pharmacists_address) private{
        for (uint i = 0; i < _pharmacists_address.length; i++) {
            pharmacist_address_map[_pharmacists_address[i]]=true;
        }
        pharmacists = _pharmacists_address;
    }

    constructor(
        address _patient_address,
        address[] memory _pharmacists_address,
        string memory _directions,
        string memory _quantity,
        string memory _date,
        string memory _name,
        string memory _strength,
        string memory _formulation
    ) {
        creator = msg.sender;
        drug = Drug(_name, _strength, _formulation);
        patient_address = _patient_address;
        directions = _directions;
        quantity = _quantity;
        date = _date;
        setPharmacists(_pharmacists_address);
        isUsed = false;
        isPatientSigned = false;
    }

    function patientSign(address _pharmacist) public returns (bool) {
        require(!isPatientSigned && msg.sender == patient_address);
        isPatientSigned = true;

        return isPatientSigned;
    }

    function getPrescription()
        public
        view
        returns (
            address,
            address[] memory,
            string memory,
            string memory,
            string memory,
            string memory,
            string memory,
            string memory,
            bool,
            bool) {
        require(pharmacist_address_map[msg.sender]
            || msg.sender == patient_address
            || msg.sender == creator
        );
        return (
            patient_address,
            pharmacists,
            directions,
            quantity,
            date,
            drug.name,
            drug.strength,
            drug.formulation,
            isUsed,
            isPatientSigned
        );
    }

    function redeem() public returns (bool) {
        require(!isUsed && pharmacist_address_map[msg.sender]);

        isUsed = true;
        prescriptionRedeemedAt = msg.sender;
        return (isUsed);
    }

}
