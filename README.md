# Secure Medical Blockchain Integration (Corda + Hedera)

This repository contains the complete integrated prototype for secure medical document integrity verification.

## Project Structure
- **`Partner_A/`**: Python module for document hashing, pseudonymization, and off-chain storage.
- **`Partner_B/`**: 
  - `cordapp-template-java/`: The Corda permissioned blockchain module (States, Contracts, Flows).
  - `corda-bridge-server/`: A Spring Boot REST API that acts as the integration bridge between Python and Corda.
- **`Partner_C/`**: Python test data generator for deterministic testing scenarios.
- **`integration_test.py`**: The end-to-end demo script that sends Partner A's data to Partner B's Spring Boot bridge.

## How to Run the Integration Demo
1. Start the Corda nodes (`./gradlew deployNodes` then `./build/nodes/runnodes`).
2. Start the Spring Boot bridge server in IntelliJ.
3. Run `python integration_test.py`.