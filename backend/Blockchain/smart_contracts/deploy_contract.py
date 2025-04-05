from web3 import Web3
import json
import os

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

if not w3.is_connected():
    raise Exception("❌ Unable to connect to the Ethereum network. Please check Ganache.")

# Load compiled contract
BASE_DIR = os.path.dirname(__file__)

contract_path = os.path.join(BASE_DIR, "compiled_contract.json")



with open(contract_path, "r") as file:
    compiled_sol = json.load(file)

# Get contract ABI and Bytecode
contract_key = "contracts"
file_key = "Voting.sol"
contract_name = "Voting"

if file_key not in compiled_sol[contract_key] or contract_name not in compiled_sol[contract_key][file_key]:
    raise Exception("❌ Contract ABI and bytecode not found. Ensure the Solidity file is compiled properly.")

abi = compiled_sol[contract_key][file_key][contract_name]["abi"]
bytecode = compiled_sol[contract_key][file_key][contract_name]["evm"]["bytecode"]["object"]

# Get the first account from Ganache
account = w3.eth.accounts[0]

# Deploy contract
Voting = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = Voting.constructor().transact({"from": account})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Save contract address
contract_address = tx_receipt.contractAddress
print(f"✅ Contract deployed at {contract_address}")

# Define contract address output file
contract_address_path = os.path.join(BASE_DIR ,"contract_address.txt")

with open(contract_address_path, "w") as file:
    file.write(contract_address)

print(f"✅ Contract address saved to {contract_address_path}")
