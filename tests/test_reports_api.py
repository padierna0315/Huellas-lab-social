import pytest
from fastapi.testclient import TestClient
from src.lims_vet.main import app
from src.lims_vet.core.database import get_db

# We can mock the DB session for the test
class MockSession:
    def __init__(self):
        self.added = []
    def add(self, obj):
        self.added.append(obj)
    async def commit(self):
        pass
    async def refresh(self, obj):
        # assign an ID
        from uuid import uuid4
        obj.id = uuid4()

async def override_get_db():
    yield MockSession()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_upload_report_pdf():
    # Mock PDF content
    pdf_content = b"%PDF-1.4 mock content"
    filename = "@Max - Ana - Vet.pdf"
    
    response = client.post(
        "/api/v1/reports/upload",
        files={"file": (filename, pdf_content, "application/pdf")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["analizavet_version"] == "1.0"
    assert data["sample"]["patient"] == "Max"
    assert data["sample"]["owner"] == "Ana"
    assert data["sample"]["status"] == "RECEIVED"
    assert "meta" in data
    assert data["meta"]["source"] == "Huellas Lab Social LIMS"

def test_upload_report_not_pdf():
    response = client.post(
        "/api/v1/reports/upload",
        files={"file": ("report.txt", b"plain text", "text/plain")}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF files are supported."
