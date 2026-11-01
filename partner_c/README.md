
# Partner C — Medical Document Test Data Generator

## Purpose

This module generates fictional medical reports and a JSON manifest
for testing document integrity in a university project involving
Corda and Hedera.

It generates test data only. It does not implement blockchain
transactions or document verification.

## Requirements

- Python 3
- pytest

## Installation

Install the required dependency:

    python -m pip install -r requirements.txt

## Generate test data

From the partner_c directory, run:

    python generate_test_data.py

The command creates three fictional medical reports and
test_manifest.json.

## Test scenarios

- original: the original report matches its reference hash.
- modified: the report has been changed.
- different_document: a separate report has different contents.
- missing: the manifest references a nonexistent file.

## Expected results

PASS, FAIL and ERROR are expected outcomes for future integrity
tests. They are not actual results from a blockchain application.

## Automated tests

Run:

    python -m pytest -v

## Integration with Partner A

Partner A can use the generated reports to test SHA-256 hashing
and document integrity verification.

## Integration with Partner B

Partner B can use the case identifiers and document hashes as
inputs for testing Corda proof recording and retrieval.

The generator does not publish anything to Corda or Hedera.
