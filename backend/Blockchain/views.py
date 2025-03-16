from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .smart_contracts.utils import add_candidate, get_votes_by_candidate, vote
from web3 import Web3
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from App.models import *
from .serializers import *
from rest_framework import status



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
        
            # Debug: Print incoming request data
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
            # Debug: Print validated data
            print(f"Adding candidate: {name}, Account: {account}")
            result = add_candidate(name, account)
            return Response({"message": result}, status=201)
        elif action == "vote":
            candidate_id = request.data.get("candidate_id")
            voter_id = int(request.data.get("voter_id"))

            print("Voter id " , voter_id)



            account = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
            # Validate inputs
            if candidate_id is None:
                return Response({"error": "Candidate ID is required"}, status=400)
            if not isinstance(candidate_id, int):
                return Response({"error": "Candidate ID must be an integer"}, status=400)
            if not voter_id:
                return Response({"error": "Voter ID is required"}, status=400)
            if not account or not Web3.is_address(account):
                return Response({"error": "Valid Ethereum account is required"}, status=400)
            # Debug: Print validated data
            print(f"Voting: Candidate ID: {candidate_id}, Voter ID: {voter_id}, Account: {account}")

            try :

                result = vote(candidate_id, voter_id, account)

            except : 

                return Response({"message" : "You have already Voted"})
            
            return Response({"message": result}, status=201)
        else:
            return Response({"error": "Invalid action. Use 'add_candidate' or 'vote'."}, status=400)

   


   

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