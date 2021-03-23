from web3 import Web3, HTTPProvider
from solcx import compile_source


def compile_source_contract(contract_file_path):
    with open(contract_file_path, "r") as f:
        source = f.read()

    contract_id, contract_interface = compile_source(source).popitem()
    return contract_interface


def get_contract(w3, contract_interface, address):
    return w3.eth.contract(address=address, abi=contract_interface["abi"])


def deploy_contract(w3, contract_interface, from_account, contractsVariables):
    tx_hash = (
        w3.eth.contract(
            abi=contract_interface["abi"], bytecode=contract_interface["bin"]
        )
        .constructor(
            contractsVariables[0],
            contractsVariables[1],
            contractsVariables[2],
            contractsVariables[3],
            contractsVariables[4],
            contractsVariables[5],
            contractsVariables[6],
        )
        .transact({"from": from_account})
    )

    return w3.eth.getTransactionReceipt(tx_hash)["contractAddress"]
