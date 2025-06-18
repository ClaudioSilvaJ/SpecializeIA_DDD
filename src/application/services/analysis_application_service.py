from typing import List

from src.domain.services.symptom_matcher_service import SymptomMatcherService
from src.domain.services.specialty_predictor_service import SpecialtyPredictorService
from src.domain.models.symptom import Symptom
from src.infrastructure.external_services.i_llm_adapter import ILLMAdapter
from src.application.dtos.analysis_request_dto import AnalysisRequestDTO
from src.application.dtos.analysis_response_dto import AnalysisResponseDTO

class AnalysisApplicationService:
    def __init__(self, 
                 symptom_matcher: SymptomMatcherService, 
                 specialty_predictor: SpecialtyPredictorService,
                 llm_adapter: ILLMAdapter):
        self._symptom_matcher = symptom_matcher
        self._specialty_predictor = specialty_predictor
        self._llm_adapter = llm_adapter

    async def analyze_symptoms(self, request_dto: AnalysisRequestDTO) -> AnalysisResponseDTO:
        llm_extracted_text = await self._llm_adapter.extract_symptoms_from_message(request_dto.message)
        matched_symptoms: List[Symptom] = self._symptom_matcher.find_matching_symptoms(llm_extracted_text)
        suggested_specialties_models = []
        if matched_symptoms:
            suggested_specialties_models = self._specialty_predictor.predict_specialties(matched_symptoms)
        symptom_names = [s.name for s in matched_symptoms] if matched_symptoms else ["Nenhum"]
        specialty_names = [sp.name for sp in suggested_specialties_models]

        return AnalysisResponseDTO(
            extracted_symptoms=symptom_names,
            suggested_specialties=specialty_names
        )

