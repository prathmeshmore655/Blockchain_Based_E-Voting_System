from solcx import compile_standard, install_solc
import json
import os

# Install Solidity Compiler (Only if not installed)
SOLC_VERSION = "0.8.0"
install_solc(SOLC_VERSION)

# Get base directory
BASE_DIR = os.path.dirname(__file__)

contract_path = os.path.join(BASE_DIR, "Voting.sol")

try:
    # Read the Solidity contract
    with open(contract_path, "r") as file:
        voting_contract = file.read()

    # Compile the contract
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"Voting.sol": {"content": voting_contract}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": [
                            "abi",
                            "metadata",
                            "evm.bytecode",  # Compiled bytecode
                            "evm.bytecode.sourceMap",
                            "evm.deployedBytecode",  # Deployed bytecode
                            "evm.deployedBytecode.sourceMap",
                        ]
                    }
                }
            },
        },
        solc_version=SOLC_VERSION,
    )

    # Define output path for compiled contract
    compiled_contract_path = os.path.join(BASE_DIR, "compiled_contract.json")

    # Save the compiled contract as JSON
    with open(compiled_contract_path, "w") as file:
        json.dump(compiled_sol, file, indent=4)

    print("✅ Smart contract compiled successfully!")

except FileNotFoundError:
    print("❌ Error: Solidity contract file 'Voting.sol' not found.")
except Exception as e:
    print(f"❌ Compilation failed: {e}")
