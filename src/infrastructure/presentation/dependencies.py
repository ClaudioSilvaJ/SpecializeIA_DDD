#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from functools import lru_cache

from src.domain.services.symptom_matcher_service import SymptomMatcherService
from src.domain.services.specialty_predictor_service import SpecialtyPredictorService
from src.application.services.analysis_application_service import AnalysisApplicationService
from src.infrastructure.persistence.csv_symptom_repository import CsvSymptomRepository
from src.infrastructure.persistence.pkl_specialty_prediction_model_repository import PklSpecialtyPredictionModelRepository
from src.infrastructure.external_services.ollama_adapter import OllamaAdapter
from src.infrastructure.external_services.i_llm_adapter import ILLMAdapter
from src.domain.repositories.i_symptom_repository import ISymptomRepository
from src.domain.repositories.i_specialty_prediction_model_repository import ISpecialtyPredictionModelRepository 


SRC_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_ROOT = os.path.dirname(SRC_DIR)
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")

VARIATIONS_CSV_PATH = os.path.join(ASSETS_DIR, "datasets", "sintomas_variacoes.csv")
WEIGHTS_CSV_PATH = os.path.join(ASSETS_DIR, "datasets", "Sintomas_pesos.csv")
MODEL_PKL_PATH = os.path.join(ASSETS_DIR, "model", "modelo_logistico_traduzido.pkl")

@lru_cache()
def get_symptom_repository() -> CsvSymptomRepository:
    """Provides a singleton instance of the CsvSymptomRepository."""
    return CsvSymptomRepository(
        variations_path=VARIATIONS_CSV_PATH, 
        weights_path=WEIGHTS_CSV_PATH
    )

@lru_cache()
def get_specialty_model_repository() -> PklSpecialtyPredictionModelRepository:
    repo = PklSpecialtyPredictionModelRepository(model_path=MODEL_PKL_PATH)
    return repo

@lru_cache()
def get_llm_adapter() -> OllamaAdapter:
    return OllamaAdapter(model_name="llama3.1")

@lru_cache()
def get_symptom_matcher_service() -> SymptomMatcherService:
    return SymptomMatcherService(symptom_repository=get_symptom_repository())

@lru_cache()
def get_specialty_predictor_service() -> SpecialtyPredictorService:
    return SpecialtyPredictorService(
        model_repository=get_specialty_model_repository(),
        symptom_repository=get_symptom_repository(),
        predictions_to_return=3
    )

def get_analysis_service() -> AnalysisApplicationService:

    return AnalysisApplicationService(
        symptom_matcher=get_symptom_matcher_service(),
        specialty_predictor=get_specialty_predictor_service(),
        llm_adapter=get_llm_adapter()
    )

