from typing import Dict, Any
from uuid import UUID

class ExportService:
    @staticmethod
    def to_analizavet_format(sample_id: UUID, patient_name: str, owner_name: str, status: str, results_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Serializes sample data into the required AnalizaVet JSON format.
        """
        return {
            "analizavet_version": "1.0",
            "sample": {
                "id": str(sample_id),
                "patient": patient_name,
                "owner": owner_name,
                "status": status,
            },
            "results": results_data,
            "meta": {
                "source": "Huellas Lab Social LIMS",
                "exported_at": None # To be filled by the caller if needed
            }
        }
