from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User
from App.models import CandidateRegistration
from eth_account import Account
from web3 import Web3
import requests
from .models import EthereumAccount

# Connect to Ganache (or another Ethereum provider)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Set funder account (for sending ETH to new voter accounts)
FUNDER_ACCOUNT = w3.eth.accounts[0]  # First Ganache account
FUNDER_PRIVATE_KEY = "0x8bef2b30d28b30c09a1ed04072f0169c5789ce59a5af23ff82cc1e8aeb29c4b2"  # Replace with actual private key

# Blockchain API URL (update if needed)
BLOCKCHAIN_API_URL = "http://localhost:8000/Blockchain/blockchain-api"

### 1. Add Candidates (Political Leaders) to Blockchain ###
@receiver(post_save, sender=CandidateRegistration)
def add_candidate_to_blockchain(sender, instance, created, **kwargs):
    if created:  # Trigger only when a new candidate is registered
        data = {
            "action": "add_candidate",
            "name": instance.name,
            "account": "0xF86e7Da91C17541Ab36a082346349702ba6070A1",  # Replace with actual wallet logic
        }

        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(BLOCKCHAIN_API_URL, json=data, headers=headers)
            response.raise_for_status()  # Raise an error for 4xx or 5xx responses
            print(f"✅ Candidate {instance.name} added to blockchain successfully!")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error adding candidate to blockchain: {e}")

@receiver(post_save, sender=User)
def create_ethereum_account(sender, instance, created, **kwargs):
    if created:  # Only for new users
        acct = Account.create()

        # Store private key in plaintext (⚠️ Not secure, use a vault in production)
        EthereumAccount.objects.create(
            user=instance,
            eth_private_key=acct.key.hex(),  # No encryption
            eth_address=acct.address
        )

        print(f"✅ Created Ethereum account: {acct.address}")

        # Send ETH to voter account
        tx = {
            'to': acct.address,
            'from': FUNDER_ACCOUNT,
            'value': w3.to_wei(1, 'ether'),
            'gas': 21000,
            'gasPrice': w3.to_wei('10', 'gwei'),
            'nonce': w3.eth.get_transaction_count(FUNDER_ACCOUNT),
        }

        try:
            signed_tx = w3.eth.account.sign_transaction(tx, FUNDER_PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)  # Correct attribute
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"✅ 1 ETH sent to {acct.address} (TX: {tx_hash.hex()})")
        except Exception as e:
            print(f"❌ Error funding account: {e}")
