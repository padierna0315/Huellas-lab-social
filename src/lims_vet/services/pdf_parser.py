import re
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class PDFParserService:
    @staticmethod
    def parse_filename(filename: str) -> Dict[str, Optional[str]]:
        """
        Parses the filename to extract patient and owner names.
        Expected format example: '@Mantequilla - Ángela Zapata - Dahiana-2.pdf'
        """
        patient_name = None
        owner_name = None
        
        # Remove extension
        clean_name = re.sub(r'\.pdf$', '', filename, flags=re.IGNORECASE)
        
        # Check if it follows the pattern '@Patient - Owner ...'
        if clean_name.startswith('@'):
            parts = [p.strip() for p in clean_name.split('-')]
            if len(parts) >= 1:
                patient_name = parts[0].replace('@', '').strip()
            if len(parts) >= 2:
                owner_name = parts[1].strip()
                
        return {
            "patient_name": patient_name,
            "owner_name": owner_name
        }

    @staticmethod
    def parse_content(text: str) -> Dict[str, Any]:
        """
        Parses the internal text of the PDF.
        Extracts structured results and metadata.
        """
        results_data = {}
        
        # Very basic regex extractions for common lab parameters (mock logic to be extended)
        wbc_match = re.search(r'WBC\s+(\d+\.?\d*)', text, re.IGNORECASE)
        if wbc_match:
            results_data["WBC"] = float(wbc_match.group(1))
            
        rbc_match = re.search(r'RBC\s+(\d+\.?\d*)', text, re.IGNORECASE)
        if rbc_match:
            results_data["RBC"] = float(rbc_match.group(1))

        patient_match = re.search(r'Paciente:\s*(.+)', text, re.IGNORECASE)
        patient_name = patient_match.group(1).strip() if patient_match else None
        
        owner_match = re.search(r'Propietario:\s*(.+)', text, re.IGNORECASE)
        owner_name = owner_match.group(1).strip() if owner_match else None

        return {
            "results_data": results_data,
            "patient_name": patient_name,
            "owner_name": owner_name
        }

    @classmethod
    def dual_parse(cls, filename: str, text: str) -> Dict[str, Any]:
        """
        Implements dual-parsing strategy:
        1. Parse filename for primary identifiers.
        2. Parse internal text/metadata.
        3. Merge results, preferring filename data if available for identifiers.
        """
        filename_data = cls.parse_filename(filename)
        content_data = cls.parse_content(text)
        
        # Merge data, preferring filename extraction for patient/owner
        patient_name = filename_data.get("patient_name") or content_data.get("patient_name") or "Unknown"
        owner_name = filename_data.get("owner_name") or content_data.get("owner_name")
        
        return {
            "patient_name": patient_name,
            "owner_name": owner_name,
            "results_data": content_data.get("results_data", {})
        }
