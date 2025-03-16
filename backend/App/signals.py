from django.db.models.signals import post_save
from django.dispatch import receiver
from App.models import CandidateRegistration
import requests

@receiver(post_save, sender=CandidateRegistration)
def add_candidate_to_blockchain(sender, instance, created, **kwargs):
    if created:  # Only trigger on new candidate
        blockchain_api_url = "http://localhost:8000/Blockchain/blockchain-api"  # Adjust this to match your API URL

        data = {
            "action": "add_candidate",
            "name": instance.name,
            "account": "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1",  # Assuming `wallet_address` is stored in the Candidate model
        }

        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(blockchain_api_url, json=data, headers=headers)
            response.raise_for_status()  # Raise error for bad response (4xx, 5xx)
            print(f"✅ Candidate {instance.name} added to blockchain successfully!")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error adding candidate to blockchain: {e}")
