from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .smart_contracts.utils import add_candidate, get_votes_by_candidate, vote , get_candidate
from web3 import Web3
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from App.models import *
from .serializers import *
from rest_framework import status
import os 
import json 



w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545")) 





class BlockchainAPI(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        candidate_id = request.query_params.get("candidate_id")

        if candidate_id is not None:
            try:
                candidate_id = int(candidate_id)  # Ensure it's an integer
                result = get_votes_by_candidate(candidate_id)
                return Response(result)
            except ValueError:
                return Response({"error": "Invalid candidate ID"}, status=400)
        
        return Response({"error": "Candidate ID is required"}, status=400)







    def post(self, request):
        """
        Handles adding a candidate or casting a vote based on request data.
        """
        print(f"Incoming request data: {request.data}")

        action = request.data.get("action")  # Determine operation: "add_candidate" or "vote"

        if action == "add_candidate":
            name = request.data.get("name")
            account = request.data.get("account")

            # Validate inputs
            if not name:
                return Response({"error": "Candidate name is required"}, status=400)
            if not account or not Web3.is_address(account):
                return Response({"error": "Valid Ethereum account is required"}, status=400)

            print(f"Adding candidate: {name}, Account: {account}")
            result = add_candidate(name, account)

            return Response({"message": result}, status=201)

        elif action == "vote":
            candidate_name = request.data.get("candidate_id")

            # Ensure candidate retrieval returns an integer ID
            candidate_id_data = get_candidate(candidate_name)

            print("c_id data" , candidate_id_data)

            if not isinstance(candidate_id_data, dict) or 'id' not in candidate_id_data:
                return Response({"error": "Invalid candidate data received"}, status=400)

            candidate_id = candidate_id_data['id']
            print("Candidate ID:", candidate_id)

            try:
                voter_id = int(request.data.get("voter_id"))
                print("Voter ID:", voter_id)

                # Fetch voter's Ethereum account
                eth_account = EthereumAccount.objects.get(user_id=voter_id)

                # Ensure voter Ethereum address matches
                voter_address = request.user.ethereumaccount.eth_address
                if voter_address.lower() != eth_account.eth_address.lower():
                    return Response({"error": "Voter Ethereum account mismatch"}, status=400)

                # Ensure voter has enough ETH balance
                balance = w3.eth.get_balance(voter_address)

                print("Balance of accountant : " , balance , voter_address)
                if balance < w3.to_wei(0.01, 'ether'):
                    return Response({"error": "Insufficient balance for transaction"}, status=400)

                # Load contract address from file
                CONTRACT_PATH = os.path.join(os.path.dirname(__file__) , 'smart_contracts')
                with open(os.path.join(CONTRACT_PATH, "contract_address.txt"), "r") as file:
                    contract_address = file.read().strip()

                # Load contract ABI
                with open(os.path.join(CONTRACT_PATH, "compiled_contract.json"), "r") as file:
                    contract_data = json.load(file)

                # Load smart contract
                contract = w3.eth.contract(address=contract_address, abi=contract_data["contracts"]["Voting.sol"]["Voting"]["abi"])


                if contract.functions.hasVoted(voter_address).call():
                    return Response({"error": "Voter has already voted"}, status=400)



                # Build transaction
                tx = contract.functions.vote(candidate_id, voter_id).build_transaction({
                    "from": voter_address,
                    "nonce": w3.eth.get_transaction_count(voter_address),
                    "gas": 200000,
                    "gasPrice": w3.to_wei("10", "gwei"),
                })

                # Sign and send transaction
                signed_tx = w3.eth.account.sign_transaction(tx, eth_account.eth_private_key)
                tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)  # Correct attribute

                print(f"✅ Vote Cast - TX Hash: {tx_hash.hex()}")

                # Mark voter as voted in database
                Voter.objects.filter(user=voter_id).update(is_voted=True)

                return Response({"message": "Vote successfully cast!", "tx_hash": tx_hash.hex()}, status=200)

            except EthereumAccount.DoesNotExist:
                return Response({"error": "Voter Ethereum account not found"}, status=404)

            except Exception as e:
                return Response({"error": f"Blockchain voting failed: {str(e)}"}, status=500)

        else:
            return Response({"error": "Invalid action"}, status=400)

   


   

    def put(self, request):
        """
        Reserved for future updates (e.g., modifying election data).
        """
        return Response({"message": "PUT method not implemented"}, status=501)







class CandidatesAPI(APIView) : 


    def get (self , request) :


        data = CandidateRegistration.objects.all()

        s_data = CandidateSerializer( data , many = True)

        return JsonResponse(s_data.data , safe=False , status = status.HTTP_200_OK)
    



class VoteAPI (APIView) : 

    def get (self , request ) :

        result = []

        count = CandidateRegistration.objects.all().count()
        n_can = CandidateRegistration.objects.all()

        print("n can" , n_can)

        is_vote = Voter.objects.filter(is_voted = True).count()
        total_is_vote = Voter.objects.all().count()

        percentage = (is_vote/total_is_vote)*100


        names = list(n_can.values_list("name", flat=True))
        
        print("list names " , names)

        for n in names : 
            
            candidate_id = n  # Ensure it's an integer
            
            name_count = get_candidate(candidate_id)

            print("receiving count " , name_count.get('id'))


            result.append({
                        
                        "candidate_id" :name_count.get('id') ,
                        "name" :  name_count.get('name') ,
                        "votes" :  name_count.get('votes') ,
                     
                        
                        })


        

        return Response({
                    "candidates": result,  
                    "defined": {
                        "participation": percentage,
                        "total_voters": total_is_vote,
                        "options": count
                    }
                }, status=status.HTTP_200_OK)

    