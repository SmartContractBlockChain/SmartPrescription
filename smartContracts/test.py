from web3 import Web3, HTTPProvider
from solcx import compile_source


def compile_source_contract(contract_file_path):
    with open(contract_file_path, "r") as f:
        source = f.read()

    contract_id, contract_interface = compile_source(source).popitem()
    return contract_interface


def get_contract(w3, contract_interface, address):
    return w3.eth.contract(address=address, abi=contract_interface["abi"])


def deploy_contract(w3, contract_interface, from_account, contract_variables):
    tx_hash = (
        w3.eth.contract(
            abi=contract_interface["abi"], bytecode=contract_interface["bin"]
        )
        .constructor(
            contract_variables[0],
            contract_variables[1],
            contract_variables[2],
            contract_variables[3],
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

    # obtain address of deployed contract
    contract_varss = [
        "0x4507d86166320d0b6521dd58eDFdceEAEB5a4AeE",
        [
            "0x5ec66e0638fb4aac37775E69fdc0D1D846211d61",
            "0xE3A5B41cA5211F6946BD284D2895e79750ded115",
            "0xF74ab552812f455Bf6047397ab8088D5FFc6004e",
        ],
        "01/01/2021",
        [
            ("drugName", "drugStrength", "drugFormulation", "quantity", "Directions"),
            ("Stabilo", "10mg", "Classic", "1g", "After every meal"),
            ("Nosing", "500g", "Diabetes", "10g", "When nose sore"),
        ],
    ]
    print(
        contract_varss[0], contract_varss[1], contract_varss[2], contract_varss[3],
    )
    address = deploy_contract(
        w3, contract_interface, w3.eth.accounts[0], contract_varss
    )

    # interact with contract from blockchain
    print(
        "Your medicine is: "
        + str(
            get_contract(w3, contract_interface, address)
            .functions.getPrescription()
            .call()
        )
    )
    patient_address = contract_varss[0]

    print(
        "tx_hash of patient signing"
        + str(
            get_contract(w3, contract_interface, address)
            .functions.patientSign()
            .transact({"from": patient_address})
        )
    )

    pharmacist = contract_varss[1][0]
    print(
        "tx_hash of pharmacist redeeming:"
        + str(
            get_contract(w3, contract_interface, address)
            .functions.redeem()
            .transact({"from": pharmacist})
        )
    )
