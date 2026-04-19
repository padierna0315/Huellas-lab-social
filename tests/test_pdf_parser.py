import pytest
from src.lims_vet.services.pdf_parser import PDFParserService

def test_parse_filename_valid_format():
    filename = "@Mantequilla - Ángela Zapata - Dahiana-2.pdf"
    result = PDFParserService.parse_filename(filename)
    assert result["patient_name"] == "Mantequilla"
    assert result["owner_name"] == "Ángela Zapata"

def test_parse_filename_invalid_format():
    filename = "Report_123.pdf"
    result = PDFParserService.parse_filename(filename)
    assert result["patient_name"] is None
    assert result["owner_name"] is None

def test_parse_content_valid():
    text = "Paciente: Toby\nPropietario: Juan Perez\nWBC 12.5\nRBC 5.4"
    result = PDFParserService.parse_content(text)
    assert result["patient_name"] == "Toby"
    assert result["owner_name"] == "Juan Perez"
    assert result["results_data"] == {"WBC": 12.5, "RBC": 5.4}

def test_dual_parse_prefers_filename():
    filename = "@Luna - Pedro Garcia.pdf"
    text = "Paciente: Desconocido\nPropietario: Nadie\nWBC 10.0"
    result = PDFParserService.dual_parse(filename, text)
    assert result["patient_name"] == "Luna"
    assert result["owner_name"] == "Pedro Garcia"
    assert result["results_data"] == {"WBC": 10.0}

def test_dual_parse_fallback_to_content():
    filename = "report_test.pdf"
    text = "Paciente: Simba\nPropietario: Carlos Gomez\nWBC 8.5"
    result = PDFParserService.dual_parse(filename, text)
    assert result["patient_name"] == "Simba"
    assert result["owner_name"] == "Carlos Gomez"
    assert result["results_data"] == {"WBC": 8.5}
