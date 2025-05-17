from web3 import Web3
import json
import os

# Connect to Ethereum (Ganache or Infura)
ganache_url = "https://ganache-docker-production.up.railway.app"  # Update if using another RPC provider
w3 = Web3(Web3.HTTPProvider(ganache_url))

if not w3.is_connected():
    raise Exception("❌ Failed to connect to the Ethereum network")

# Load contract details
CONTRACT_PATH = os.path.join(os.path.dirname(__file__))

# Read contract address
with open(os.path.join(CONTRACT_PATH, "contract_address.txt"), "r") as file:
    contract_address = file.read().strip()

# Read compiled contract JSON
with open(os.path.join(CONTRACT_PATH, "compiled_contract.json"), "r") as file:
    contract_data = json.load(file)

# Extract ABI
contract = w3.eth.contract(address=contract_address, abi=contract_data["contracts"]["Voting.sol"]["Voting"]["abi"])


### 🗳️ Candidate Management ###
def add_candidate(name, account):
    """Add a candidate to the blockchain."""
    tx_hash = contract.functions.addCandidate(name).transact({"from": account})
    w3.eth.wait_for_transaction_receipt(tx_hash)
    return f"✅ Candidate '{name}' added successfully!"


### 🗳️ Voting Function (Including Voter ID) ###
def vote(candidate_id, voter_id, account):
    """Cast a vote for a candidate with voter ID."""
    tx_hash = contract.functions.vote(candidate_id, voter_id).transact({"from": account})
    w3.eth.wait_for_transaction_receipt(tx_hash)

    return f"✅ Vote casted for candidate {candidate_id} by voter {voter_id}!"


### 🗳️ Retrieve Election Results ###
def get_results():
    """Retrieve voting results."""
    num_candidates = contract.functions.getTotalCandidates().call()
    
    results = []
    for i in range(num_candidates):
        candidate = contract.functions.getVotes(i).call()  # Fetch votes
        name = contract.functions.candidates(i).call()[0]  # Fetch candidate name
        results.append({"id": i, "name": name, "votes": candidate})

        
    print(results)
    return results


### 🗳️ Get Candidate Details ###
def get_candidate(name):
    """Retrieve candidate details by ID."""

    candidate_id = get_candidate_id(name)

    if candidate_id is not None : 
        
        candidate = contract.functions.candidates(candidate_id).call()

        print("whole data " , candidate)

        return {"id": candidate_id , "name": candidate[1], "votes": candidate[2]}

    else:

        return ("No candidate exists")


### 🗳️ Check if Voter Has Voted ###
def has_voter_voted(account):
    """Check if a voter has already voted."""
    return contract.functions.hasVoterVoted(account).call()


### 🗳️ Get Voter ID ###
def get_voter_id(account):
    """Retrieve the voter ID if they have voted."""
    if not has_voter_voted(account):
        return "❌ Voter has not voted yet."
    
    return contract.functions.getVoterId(account).call()


def get_votes_by_candidate(candidate_id):
    """Retrieve vote count for a specific candidate."""
    try:
        votes = contract.functions.getVotes(candidate_id).call()
        return {"candidate_id": candidate_id, "votes": votes}
    except Exception as e:
        return {"error": str(e)}
    

# c_id , v_id , account

def get_candidate_id(name):
    """Fetch candidate ID by name from blockchain"""
    candidates = contract.functions.getCandidates().call()  # Get all candidates from blockchain
    
    for idx, candidate in enumerate(candidates):
        if candidate == name:

            print(idx)

            return idx  # Return the correct ID

    
    print("none")
    
    return None  # Candidate not found



get_candidate_id("Narendra Modi")