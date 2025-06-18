from pydantic import BaseModel
from typing import List

class AnalysisResponseDTO(BaseModel):
    extracted_symptoms: List[str]
    suggested_specialties: List[str]

