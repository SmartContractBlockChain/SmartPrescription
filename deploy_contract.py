from web3 import Web3
from solc import compile_files


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# compile all contract files
contracts = compile_files(['prescription.sol'])

main_contract = contracts.pop("prescription.sol:Prescription")
