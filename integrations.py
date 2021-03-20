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


if __name__ == "__main__":
    blockchain_address = "HTTP://127.0.0.1:7545"
    w3 = Web3(HTTPProvider(blockchain_address))

    # compile contract
    contract_source_path = "smartContracts/Prescription.sol"
    contract_interface = compile_source_contract(contract_source_path)

    # We set the variable for the contract definition
    _contractVariables = [
        w3.eth.accounts[0],
        "directions",
        "quantity",
        "01/01/2021",
        "drugName",
        "drugStrength",
        "drugFormulation",
    ]

    # obtain address of deployed contract
    address = deploy_contract(
        w3, contract_interface, w3.eth.accounts[0], _contractVariables
    )
    """address = w3.eth.getTransactionReceipt(
        0x41EF0DFC2B96FD2F06393F4A3D1F53C967834EC9F83BF1F0C3A63F59CCD8F6E5
    )["contractAddress"]"""

    print(f"your contraact address is {address}")
    # interact with contract from blockchain
    print(
        "Your medicine is: "
        + str(get_contract(w3, contract_interface, address).functions.redeem().call())
    )
# get_contract(w3, contract_interface, address).functions._functions) get all the avail functions
