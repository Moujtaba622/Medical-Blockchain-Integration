import json
import requests
import os
import sys

# =====================================================================
# ⚙️ CONFIGURATION: PUT YOUR EXACT FOLDER PATHS HERE (Use forward slashes /)
# =====================================================================
PARTNER_A_DIR = "C:/Users/ghris/Downloads/blockchain-yecine-main/blockchain-yecine-main/partner_a"  
PARTNER_C_FILE = "C:/Users/ghris/Downloads/partner_c-20261031T160658Z-1-001/partner_c/test_data" # <-- The text file
# =====================================================================

# 1. Tell Python to look inside Partner A's folder for imports
sys.path.append(PARTNER_A_DIR)
from document_service import store_document, DocumentServiceError

print("🚀 STARTING FULL END-TO-END INTEGRATION DEMO 🚀\n")

# 2. Partner C's file check
if not os.path.exists(PARTNER_C_FILE):
    print(f"❌ Error: Cannot find Partner C's file at {PARTNER_C_FILE}")
    sys.exit(1)
print(f"✅ [Partner C] Found document at: {PARTNER_C_FILE}")

# 3. Partner A's hashing
print("\n⏳ [Partner A] Running store_document()...")
try:
    # We tell Partner A to store the file in a temporary folder on your desktop
    partner_a_data = store_document(
        source_path=PARTNER_C_FILE,
        case_id="CASE-999",
        artifact_id="DOC-999",
        document_type="lab_report",
        storage_dir="C:/Users/ghris/Desktop/secure_storage" 
    )
    print("✅ [Partner A] Successfully hashed and stored the document.")
    print(json.dumps(partner_a_data, indent=2))

except DocumentServiceError as e:
    print(f"❌ [Partner A] Error: {e}")
    sys.exit(1)

# 4. The Bridge (Send to Spring Boot)
print("\n⏳ [Bridge] Sending data to Corda via Spring Boot...")

# ONLY send the 5 fields Corda expects
corda_payload = {
    "case_id": partner_a_data["case_id"],
    "artifact_id": partner_a_data["artifact_id"],
    "document_hash": partner_a_data["document_hash"],
    "document_type": partner_a_data["document_type"],
    "created_at": partner_a_data["created_at"]
}

try:
    response = requests.post("http://localhost:8080/api/recordProof", json=corda_payload, timeout=10)
    
    if response.status_code == 200:
        print("✅ [Partner B] Corda responded successfully!")
        print("Response:", response.text)
    else:
        print(f"❌ [Partner B] Bridge returned error status: {response.status_code}")
        print(response.text)

except requests.exceptions.ConnectionError:
    print("❌ [Bridge] Could not connect to Spring Boot. Is the Spring Boot server running on port 8080?")
except requests.exceptions.Timeout:
    print("❌ [Bridge] Spring Boot timed out. Check the IntelliJ console for errors (did you downgrade to Spring Boot 2.7.18?)")