from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict
import io
import datetime

try:
    import pypdf
except ImportError:
    pypdf = None

from ...core.database import get_db
from ...models.sample import Sample, SampleStatus
from ...services.pdf_parser import PDFParserService
from ...services.export import ExportService

router = APIRouter(prefix="/reports", tags=["reports"])

@router.post("/upload", response_model=Dict[str, Any])
async def upload_report(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Receives a PDF, parses it via dual-parsing (filename + text),
    creates a Sample in the database, and returns the AnalizaVet JSON format.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    content = await file.read()
    
    # Extract text from PDF
    text = ""
    if pypdf:
        try:
            pdf_reader = pypdf.PdfReader(io.BytesIO(content))
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            text = f"[PDF Extraction Error: {e}]"
    else:
        text = "[pypdf not installed, text extraction disabled]"

    # Dual parsing: filename and internal text
    parsed_data = PDFParserService.dual_parse(file.filename, text)
    
    # Create the Sample in the db
    new_sample = Sample(
        patient_name=parsed_data.get("patient_name", "Unknown"),
        owner_name=parsed_data.get("owner_name"),
        status=SampleStatus.RECEIVED,
        results_data=parsed_data.get("results_data", {}),
        raw_text=text
    )
    
    db.add(new_sample)
    await db.commit()
    await db.refresh(new_sample)
    
    # Format and return the result using ExportService
    export_data = ExportService.to_analizavet_format(
        sample_id=new_sample.id,
        patient_name=new_sample.patient_name,
        owner_name=new_sample.owner_name,
        status=new_sample.status.value,
        results_data=new_sample.results_data
    )
    
    export_data["meta"]["exported_at"] = datetime.datetime.utcnow().isoformat()
    return export_data
