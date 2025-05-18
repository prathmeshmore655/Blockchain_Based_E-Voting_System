#!/bin/bash

# Step 1: Compile the smart contract
python Blockchain/smart_contracts/compile_contract.py

# Step 2: Deploy the smart contract
python Blockchain/smart_contracts/deploy_contract.py

# Step 3: Start the Django server
python manage.py runserver 0.0.0.0:8000
