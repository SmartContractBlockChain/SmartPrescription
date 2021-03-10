import json
from web3 import Web3, HTTPProvider
from solcx import compile_source


# truffle development blockchain address
blockchain_address = 'http://127.0.0.1:8545'

# Client instance to interact with the blockchain
web3 = Web3(HTTPProvider(blockchain_address))

# Set the default account
web3.eth.defaultAccount = web3.eth.accounts[0]

# Path to the compiled contract JSON file
compiled_contract_path = 'build/contracts/Prescription.json'

# Deployed contract address (see `migrate` command output: `contract address`)
deployed_contract_address = '0x802fAd8226580F34b38323D4273a7cdbaDD79872'

with open(compiled_contract_path) as file:
    contract_json = json.load(file)  # load contract info as JSON
    contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

# Fetch deployed contract reference
contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

print(contract.address)

# Call contract function (this is not persisted to the blockchain)
# message = contract.functions.getmedicineName().call()

print(contract.functions)
