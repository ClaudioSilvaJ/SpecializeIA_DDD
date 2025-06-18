from pydantic import BaseModel

class AnalysisRequestDTO(BaseModel):
    message: str

