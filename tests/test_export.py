import pytest
from uuid import uuid4
from src.lims_vet.services.export import ExportService

def test_to_analizavet_format():
    sample_id = uuid4()
    patient_name = "Rex"
    owner_name = "Maria"
    status = "RECEIVED"
    results_data = {"WBC": 11.0, "RBC": 4.5}

    result = ExportService.to_analizavet_format(
        sample_id=sample_id,
        patient_name=patient_name,
        owner_name=owner_name,
        status=status,
        results_data=results_data
    )

    assert result["analizavet_version"] == "1.0"
    assert result["sample"]["id"] == str(sample_id)
    assert result["sample"]["patient"] == "Rex"
    assert result["sample"]["owner"] == "Maria"
    assert result["sample"]["status"] == "RECEIVED"
    assert result["results"] == results_data
    assert result["meta"]["source"] == "Huellas Lab Social LIMS"
    assert result["meta"]["exported_at"] is None
