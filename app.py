import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random
from web3 import Web3, HTTPProvider
from solcx import compile_source
from helpers import compile_source_contract, get_contract, deploy_contract


def create_app(test_config=None):
    # Defining global variables
    blockchain_address = "HTTP://127.0.0.1:7545"  # Change to local blockchain address
    w3 = Web3(HTTPProvider(blockchain_address))
    contract_source_path = "smartContracts/Prescription.sol"
    contract_interface = compile_source_contract(contract_source_path)

    # create and configure the app
    app = Flask(__name__)
    # Set up CORS. Allow '*' for origins.
    CORS(app, resources={r"/api/*": {"origins": "*"}})

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

    """
    GET requests for drugs list.

    Retrieve drugs list 
    * name 
    * availability (optional) 

    Authorized users (Doctor and Pharmacist)
    """

    @app.route("/drugs")
    def get_drugs_list():

        return jsonify({"success": True,}), 200

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

        return jsonify({"success": True,}), 200

    """
    GET requests for prescription.

    Retrieve prescription details by the contract transaction hash
    * patient_address
    * drug name
    * directions
    * quantity
    * signature  (name and address of prescriber)
    * date of issue 
    * isUsed (boolean) 
    
    Authorized users (Doctor, Pharmacist and Patient)
    """

    @app.route("/prescription/<string:address>")
    def get_prescription(address):
        prescription = (
            get_contract(w3, contract_interface, address)
            .functions.getPrescription()
            .call()  # .call({'from':web3.eth.accounts[1]}) to select the wallet from which to call the function
        )
        return jsonify({"success": True, "Prescription": prescription}), 200

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

        return jsonify({"success": True, "Prescriber": creator}), 200

    """
    POST requests for creating prescription.

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
        _contractVariables = [
            request_data["patientAddress"],
            request_data["directions"],
            request_data["quantity"],
            request_data["date"],
            request_data["drugName"],
            request_data["drugStrength"],
            request_data["drugFormulation"],
        ]
        address = deploy_contract(
            w3, contract_interface, w3.eth.accounts[0], _contractVariables
        )
        return jsonify({"success": True, "contractAddress": address}), 200

    """
    POST requests for redeem prescription.

    Redeem prescription
    * patient_address
    * setPharmacist
    * check isUsed
        - if true --> reject the request
        - if false --> 1) accsept the request and 2) set isUsed to true
        
    Authorized users (Pharmacist)

    NOTE: check of the variable in the request to use wither patient_address or pharmacist_address
    """

    @app.route("/redeem/<string:address>", methods=["POST"])
    def redeem_prescription(address):
        isUsed = get_contract(w3, contract_interface, address).functions.redeem().call()
        return jsonify({"success": True, "Prescription used": isUsed}), 200

    """
    POST requests for redeem prescription.

    Redeem prescription
    * patient_address
    * setPharmacist
    * check isUsed
        
    Authorized users (Patient)
    """

    @app.route("/sign/<string:address>")
    def patient_sign(address):
        patient_address = request.args.get("patient", None)
        isSigned = (
            get_contract(w3, contract_interface, address)
            .functions.patientSign()
            .call({"from": patient_address})
        )
        return jsonify({"success": True, "Patient signed": isSigned}), 200

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
