from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from web3 import Web3, HTTPProvider

from databaseManager import DataBaseManager
from smartContractUtils import compile_source_contract, get_contract, deploy_contract
from flask_mysqldb import MySQL


def create_app(test_config=None):
    # Defining global variables
    blockchain_address = 'http://127.0.0.1:8545'  # Change to local blockchain address
    w3 = Web3(HTTPProvider(blockchain_address))
    contract_source_path = "smartContracts/Prescription.sol"
    contract_interface = compile_source_contract(contract_source_path)

    # create and configure the app
    app = Flask(__name__)
    # Set up CORS. Allow '*' for origins.
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # db config
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'SCBC'
    app.config['MYSQL_PASSWORD'] = 'SCBC_PASS'
    app.config['MYSQL_DB'] = 'smartPrescription'

    # db manager
    db_manager = DataBaseManager(MySQL(app))

    # after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization, true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, PUT, POST, DELETE, OPTIONS"
        )
        return response

    # TODO verify if this is needed
    """
    GET requests for drugs list.

    Retrieve drugs list 
    * name 
    * availability (optional) 

    Authorized users (Doctor and Pharmacist)
    """

    @app.route("/drugs")
    def get_drugs_list():
        return jsonify({"success": True, }), 200

    # TODO verify if this is needed
    """
    GET requests for drug information.

    Retrieve drug information by drug_name
    * name 
    * strength
    * formulation
    * availability (optional) 
    
    Authorized users (Doctor and Pharmacist)
    """

    @app.route("/drugs/<string:drug_name>")
    def get_drug_by_name(drug_name):
        return jsonify({"success": True, }), 200

    """
    GET requests for prescription.
    Required parameters in request: name, surname and userType
    Example: http://127.0.0.1:5000/prescriptions?name=Kajetan&surname=Dymkiewicz&userType=Doctor

    Retrieve prescriptions and corresponding details by user name and surname
    * patient_address
    * list of pharmacists
    * directions
    * quantity
    * date
    * drug name
    * drug strength
    * drug formulation
    * isUsed
    * isPatientSigned  
    
    Authorized users (Doctor, Pharmacist and Patient)
    """

    @app.route("/prescriptions")
    def get_prescriptions():
        name = request.args.get('name')
        surname = request.args.get('surname')
        user_type = request.args.get('userType')

        user_address = db_manager.get_user_address(name, surname, user_type)
        prescription_addresses = db_manager.get_prescriptions_by_type(name, surname, user_type)

        prescriptions = {}
        for address in prescription_addresses:
            prescriptions[address] = get_contract(w3, contract_interface, address) \
                .functions.getPrescription() \
                .call({'from': user_address})

        return jsonify({"success": True, "Prescriptions": prescriptions}), 200

    # TODO verify if this is needed
    """
    GET requests for prescriber infromation.

    Retrieve prescriber infromation by the signature
    * prescriber name
    * address
    
    Authorized users (Doctor and Pharmacist)
    """

    @app.route("/prescriber/<string:address>")
    def get_prescriber(address):
        creator = (
            get_contract(w3, contract_interface, address).functions.creator().call()
        )
        return jsonify({"success": True, "creator": creator}), 200

    """
    POST requests for creating prescription.

    Required parameters in request: doctorName, doctorSurname, patientName and patientSurname

    Required parameters in body: directions, quantity, date, drugName, drugStrength, drugFormulation
    
    Example: curl --header "Content-Type: application/json" --request POST --data '{"directions":"eat it",
    "quantity":"very much","date":"today","drugName":"viagra","drugStrength":"very strong","drugFormulation":"just 
    buy it"}' http://127.0.0.1:5000/prescription\?doctorName\=Kajetan\&doctorSurname\=Dymkiewicz\&patientName\=Peter
    \&patientSurname\=McBurney 
    
    create prescription
    * patient_address
    * directions
    * quantity
    * date
    * drug 
        - name 
        - strength
        - formulation
    * date of issue
    
    Authorized user (Doctor)
    """

    @app.route("/prescription", methods=["POST"])
    def create_prescription():
        request_data = request.get_json()
        doctor_name = request.args.get('doctorName')
        doctor_surname = request.args.get('doctorSurname')

        doctor_account = db_manager.get_user_address(doctor_name, doctor_surname, 'Doctor')

        patient_name = request.args.get('patientName')
        patient_surname = request.args.get('patientSurname')

        patient_account = db_manager.get_user_address(patient_name, patient_surname, 'Patient')

        pharmacists_addresses = db_manager.get_all_pharmacists_addresses()

        _contractVariables = [
            patient_account,
            pharmacists_addresses,
            request_data["directions"],
            request_data["quantity"],
            request_data["date"],
            request_data["drugName"],
            request_data["drugStrength"],
            request_data["drugFormulation"],
        ]
        prescription_address = deploy_contract(
            w3, contract_interface, doctor_account, _contractVariables
        )

        db_manager.save_prescription(prescription_address, doctor_account, patient_account)

        return jsonify({"success": True, }), 200

    """
    POST requests for redeem prescription.
    
    Required parameters in request: name, surname and prescription_address
    
    Example: curl --request POST http://127.0.0.1:5000/redeem\?name\=Aya\&surname\=Khashoggi\&
    prescription_address\=0x43674E64Cc33183A9E4cDBDCaDAf19bDE5EACF90

    Redeem prescription
    * setPharmacist
    * check isUsed
        - if true --> reject the request
        - if false --> 1) accsept the request and 2) set isUsed to true
        
    Authorized users (Pharmacist)

    """

    @app.route("/redeem", methods=["POST"])
    def redeem_prescription():
        pharmacist_name = request.args.get('name')
        pharmacist_surname = request.args.get('surname')

        pharmacist_address = db_manager.get_user_address(pharmacist_name, pharmacist_surname, 'Pharmacist')
        prescription_address = request.args.get('prescription_address')

        tx_hash = (
            get_contract(w3, contract_interface, prescription_address)
                .functions.redeem()
                .transact({"from": pharmacist_address})
        )
        # TODO: check status and return different if transaction is False
        status = w3.eth.getTransactionReceipt(tx_hash)["status"]

        db_manager.set_pharmacist_in_contract(pharmacist_address, prescription_address)

        return jsonify({"success": True, "PrescriptionUsed": status}), 200

    """
    POST requests for redeem prescription

    Patient sign the prescription:
    * pass the address of the patient in JSON POST request
    * The call of the function is made from patient address 

    - RETURN: the status of the signature of the patient 
        
    Authorized users (Patient)
    """

    @app.route("/sign", methods=["POST"])
    def patient_sign():
        request_data = request.get_json()
        patient_address = request_data["patientAddress"]
        address = request_data["contractAddress"]
        tx_hash = (
            get_contract(w3, contract_interface, address)
                .functions.patientSign()
                .transact({"from": patient_address})
        )
        status = w3.eth.getTransactionReceipt(tx_hash)["status"]
        return jsonify({"success": True, "patientSigned": status}), 200

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
