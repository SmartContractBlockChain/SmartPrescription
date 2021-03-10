from web3 import Web3, HTTPProvider
from solcx import compile_source


def compile_source_file(file_path):
    with open(file_path, 'r') as f:
        source = f.read()

    return compile_source(source)


def get_contract(w3, contract_interface,address):
    return w3.eth.contract(address=address,
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin'])


def deploy_contract(w3, contract_interface):
    tx_hash = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']).constructor().transact()

    address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
    return address


if __name__ == '__main__':
    blockchain_address = 'http://127.0.0.1:8545'
    w3 = Web3(HTTPProvider(blockchain_address))
    w3.eth.defaultAccount = w3.eth.accounts[0]

    contract_source_path = 'contracts/Prescription.sol'
    compiled_sol = compile_source_file(contract_source_path)

    contract_id, contract_interface = compiled_sol.popitem()

    address = deploy_contract(w3, contract_interface)
    print(f'Deployed {contract_id} to: {address}\n')
