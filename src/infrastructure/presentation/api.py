from fastapi import FastAPI, HTTPException, Depends
import logging
import uvicorn
import os

from src.application.dtos.analysis_request_dto import AnalysisRequestDTO
from src.application.dtos.analysis_response_dto import AnalysisResponseDTO
from src.application.services.analysis_application_service import AnalysisApplicationService
from src.infrastructure.presentation.dependencies import get_analysis_service

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Symptom Analysis API (DDD)",
    description="API to analyze symptoms from text and suggest medical specialties, refactored with DDD.",
    version="1.0.0"
)

@app.post("/analyze-symptoms", response_model=AnalysisResponseDTO)
async def analyze_symptoms_endpoint(
    request: AnalysisRequestDTO,
    analysis_service: AnalysisApplicationService = Depends(get_analysis_service)
):
    logger.info(f"Received request for symptom analysis: {request.message[:50]}...")
    try:
        response_dto = await analysis_service.analyze_symptoms(request)
        logger.info(f"Analysis complete. Symptoms: {response_dto.extracted_symptoms}, Specialties: {response_dto.suggested_specialties}")
        return response_dto
    except FileNotFoundError as e:
        logger.error(f"Configuration file error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: Missing required data file. {e}")
    except RuntimeError as e:
        logger.error(f"Runtime error during analysis: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during analysis: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected internal server error occurred.")

def run_api():
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    logger.info(f"Starting API server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)

# if __name__ == "__main__":
#     run_api()