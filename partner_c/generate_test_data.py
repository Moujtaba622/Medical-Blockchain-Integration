
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "test_data"
MANIFEST_PATH = BASE_DIR / "test_manifest.json"

ORIGINAL = """FICTIONAL MEDICAL REPORT
Case ID: CASE-001
Patient: Test Patient A
Diagnosis: Fictional condition A
Treatment: Fictional treatment A
"""

MODIFIED = ORIGINAL.replace(
    "Fictional treatment A",
    "Fictional treatment B"
)

SECOND = """FICTIONAL MEDICAL REPORT
Case ID: CASE-002
Patient: Test Patient B
Diagnosis: Fictional condition B
Treatment: Fictional treatment C
"""


def generate_test_data():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    documents = {
        "original_report.txt": ORIGINAL,
        "modified_report.txt": MODIFIED,
        "second_report.txt": SECOND,
    }

    for filename, content in documents.items():
        (DATA_DIR / filename).write_text(
            content, encoding="utf-8"
        )

    manifest = [
        {
            "test_case_id": "TEST-001",
            "description": "Original document matches its reference",
            "case_id": "CASE-001",
            "file_path": "test_data/original_report.txt",
            "scenario": "original",
            "expected_result": "PASS",
        },
        {
            "test_case_id": "TEST-002",
            "description": "Modified document differs from original",
            "case_id": "CASE-001",
            "file_path": "test_data/modified_report.txt",
            "scenario": "modified",
            "expected_result": "FAIL",
        },
        {
            "test_case_id": "TEST-003",
            "description": "Second document differs from first document",
            "case_id": "CASE-002",
            "file_path": "test_data/second_report.txt",
            "scenario": "different_document",
            "expected_result": "FAIL",
        },
        {
            "test_case_id": "TEST-004",
            "description": "Referenced document is absent",
            "case_id": "CASE-003",
            "file_path": "test_data/missing_report.txt",
            "scenario": "missing",
            "expected_result": "ERROR",
        },
    ]

    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=4, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("Test data generated successfully.")
    print(f"Number of test cases: {len(manifest)}")


if __name__ == "__main__":
    try:
        generate_test_data()
    except (OSError, ValueError) as error:
        print(f"Generation failed: {error}", file=sys.stderr)
        sys.exit(1)
