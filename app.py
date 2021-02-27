import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)  
  
  # Set up CORS. Allow '*' for origins.
  CORS(app, resources={r"/api/*" : {'origins': '*'}})

  # after_request decorator to set Access-Control-Allow
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
    return response

  '''
  GET requests for drugs list.

  Retrieve drugs list 
    * name 
    * availability (optional) 

  Authorized users (Doctor and Pharmacist)
  '''
  @app.route('/drugs')
  def get_drugs_list():

    return jsonify({
        'success': True,
    }),200

  '''
  GET requests for drug information.

  Retrieve drug information by drug_name
    * name 
    * strength
    * formulation
    * availability (optional) 
    
  Authorized users (Doctor and Pharmacist)
  '''
  @app.route('/drugs/<string:drug_name>')
  def get_drug_by_name(drug_name):

    return jsonify({
        'success': True,
    }),200

  '''
  GET requests for prescription.

  Retrieve prescription details by patient_address
    * drug name
    * directions
    * quantity
    * signature  (name and address of prescriber)
    * date of issue 
    * isUsed (boolean) 
    
  Authorized users (Doctor and Pharmacist)
  '''
  @app.route('/prescription/<string:patient_address>')
  def get_prescription(patient_address):

    return jsonify({
        'success': True,
    }),200


  '''
  GET requests for prescriber infromation.

  Retrieve prescriber infromation by the signature
    * prescriber name
    * address
    
  Authorized users (Doctor and Pharmacist)
  '''
  @app.route('/prescription/<string:signature>')
  def get_prescriber(signature):

    return jsonify({
        'success': True,
    }),200

  '''
  POST requests for creating prescription.

  create prescription
    * prescriber information
    * patient_address
    * drug 
        - name 
        - directions
        - quantity
    * date of issue
    
  Authorized user (Doctor)
  '''
  @app.route('/prescription', methods=['POST'])
  def create_prescription():

    return jsonify({
        'success': True,
    }),200
  
  '''
  POST requests for redeem prescription.

  Redeem prescription
    * patient_address
    * setPharmacist
    * check isUsed
        - if true --> reject the request
        - if false --> 1) accsept the request and 2) set isUsed to true
        
  Authorized users (Pharmacist)

    NOTE: check of the varibale in the request to use wither patient_address or pharmacist_address
  '''
  @app.route('/redeem/<string:patient_address>', methods=['POST']) 
  def redeem_prescription():

    return jsonify({
        'success': True,
    }),200
        
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found'
    }),404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }),422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'bad request'
    }),400
  
  return app
