
import json
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "test_data"
MANIFEST_PATH = PROJECT_DIR / "test_manifest.json"
GENERATOR = PROJECT_DIR / "generate_test_data.py"

REQUIRED_FIELDS = {
    "test_case_id",
    "description",
    "case_id",
    "file_path",
    "scenario",
    "expected_result",
}


def run_generator():
    subprocess.run(
        [sys.executable, str(GENERATOR)],
        cwd=PROJECT_DIR,
        check=True,
        capture_output=True,
        text=True,
    )


def load_manifest():
    return json.loads(
        MANIFEST_PATH.read_text(encoding="utf-8")
    )


def test_generator_creates_required_files():
    run_generator()

    assert (DATA_DIR / "original_report.txt").is_file()
    assert (DATA_DIR / "modified_report.txt").is_file()
    assert (DATA_DIR / "second_report.txt").is_file()
    assert MANIFEST_PATH.is_file()


def test_manifest_is_valid_json():
    run_generator()
    manifest = load_manifest()

    assert isinstance(manifest, list)
    assert len(manifest) == 4


def test_all_scenarios_are_present():
    run_generator()
    manifest = load_manifest()

    scenarios = {item["scenario"] for item in manifest}

    assert scenarios == {
        "original",
        "modified",
        "different_document",
        "missing",
    }


def test_all_required_fields_are_present():
    run_generator()
    manifest = load_manifest()

    for item in manifest:
        assert REQUIRED_FIELDS.issubset(item.keys())


def test_test_case_identifiers_are_unique():
    run_generator()
    manifest = load_manifest()

    ids = [item["test_case_id"] for item in manifest]

    assert len(ids) == len(set(ids))


def test_original_and_modified_differ():
    run_generator()

    original = (DATA_DIR / "original_report.txt").read_bytes()
    modified = (DATA_DIR / "modified_report.txt").read_bytes()

    assert original != modified


def test_second_report_differs_from_original():
    run_generator()

    original = (DATA_DIR / "original_report.txt").read_bytes()
    second = (DATA_DIR / "second_report.txt").read_bytes()

    assert original != second


def test_missing_document_is_not_created():
    run_generator()
    manifest = load_manifest()

    missing_cases = [
        item for item in manifest
        if item["scenario"] == "missing"
    ]

    assert len(missing_cases) == 1

    missing_path = PROJECT_DIR / missing_cases[0]["file_path"]

    assert not missing_path.exists()


def test_expected_results_match_scenarios():
    run_generator()
    manifest = load_manifest()

    expected = {
        "original": "PASS",
        "modified": "FAIL",
        "different_document": "FAIL",
        "missing": "ERROR",
    }

    for item in manifest:
        assert item["expected_result"] == expected[item["scenario"]]


def test_generation_is_reproducible():
    run_generator()

    first_documents = {
        path.name: path.read_bytes()
        for path in DATA_DIR.glob("*.txt")
    }
    first_manifest = MANIFEST_PATH.read_bytes()

    run_generator()

    second_documents = {
        path.name: path.read_bytes()
        for path in DATA_DIR.glob("*.txt")
    }
    second_manifest = MANIFEST_PATH.read_bytes()

    assert first_documents == second_documents
    assert first_manifest == second_manifest
