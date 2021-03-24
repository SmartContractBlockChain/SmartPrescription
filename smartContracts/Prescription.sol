pragma experimental ABIEncoderV2;

contract smartPrescription {
    struct Drug {
        string name;
        string strength;
        string formulation;
        string quantity;
        string directions;
    }

    // address of doctor
    address public creator;
    address patient_address;
    Drug[3] drugs;
    string date;

    //all pharmacist where patient can reedem the prescription
    address[] public pharmacists;

    bool public isUsed;

    bool public isPatientSigned;
    // address of pharmacist where patient can redeemed the prescription
    address prescriptionRedeemedAt;

    mapping(address => bool) private pharmacist_address_map;

    function setPharmacists(address[] memory _pharmacists_address) private {
        for (uint256 i = 0; i < _pharmacists_address.length; i++) {
            pharmacist_address_map[_pharmacists_address[i]] = true;
        }
    }

    constructor(
        address _patient_address,
        address[] memory _pharmacists_address,
        string memory _date,
        Drug[3] memory _drugs
    ) {
        creator = msg.sender;
        drugs[0] = _drugs[0];
        drugs[1] = _drugs[1];
        drugs[2] = _drugs[2];
        patient_address = _patient_address;

        date = _date;
        pharmacists = _pharmacists_address;
        setPharmacists(_pharmacists_address);
        isUsed = false;
        isPatientSigned = false;
    }

    function patientSign() public returns (bool) {
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
            Drug[3] memory,
            bool,
            bool
        )
    {
        require(
            pharmacist_address_map[msg.sender] ||
                msg.sender == patient_address ||
                msg.sender == creator
        );

        return (
            patient_address,
            pharmacists,
            date,
            drugs,
            isUsed,
            isPatientSigned
        );
    }

    function redeem() public returns (bool) {
        require(
            !isUsed && isPatientSigned && pharmacist_address_map[msg.sender]
        );

        isUsed = true;
        prescriptionRedeemedAt = msg.sender;
        return (isUsed);
    }
}
