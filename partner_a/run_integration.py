import json
import requests
# IMPORT PARTNER A'S ACTUAL CODE HERE
# (Change 'document_service' if their file is named differently)
from document_service import store_document 

print("1. Running Partner C's file through Partner A's code...")

# We point to the file Partner C just generated!
file_path = "C:/Users/ghris/Downloads/partner_c-20261031T160658Z-1-001/partner_c/test_data/original_report.txt" 

# Call Partner A's function to get the real hash and metadata
# (Adjust the arguments based on how their function is written)
partner_a_result = store_document(
    file_path=file_path, 
    case_id="CASE-001", 
    artifact_id="DOC-001"
)

print("Partner A generated this data:")
print(json.dumps(partner_a_result, indent=2))

print("\n2. Sending Partner A's data to your Corda Bridge...")

# Send it to your Spring Boot server
response = requests.post("http://localhost:8080/api/recordProof", json=partner_a_result)

print("\n3. Response from Corda:")
print(response.text)
