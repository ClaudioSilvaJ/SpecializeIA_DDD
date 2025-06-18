from typing import List
import numpy as np

from src.domain.models.symptom import Symptom
from src.domain.models.medical_specialty import MedicalSpecialty
from src.domain.repositories.i_symptom_repository import ISymptomRepository
from src.domain.repositories.i_specialty_prediction_model_repository import ISpecialtyPredictionModelRepository

class SpecialtyPredictorService:

    def __init__(self, 
                 model_repository: ISpecialtyPredictionModelRepository, 
                 symptom_repository: ISymptomRepository,
                 predictions_to_return: int = 3):
        self._model_repository = model_repository
        self._symptom_repository = symptom_repository
        self._predictions_to_return = predictions_to_return
        self._symptom_weights: dict[str, float] = {}
        self._all_symptoms_list: list[str] = []
        self._model_repository.load_model() 

    def _load_symptom_data_if_needed(self):
        if not self._symptom_weights:
            self._symptom_weights = self._symptom_repository.get_symptom_weights()
        if not self._all_symptoms_list:
            self._all_symptoms_list = sorted(self._symptom_repository.get_all_symptom_names())

    def _create_feature_vector(self, symptoms: List[Symptom]) -> List[float]:
        self._load_symptom_data_if_needed()
        feature_vector = [0.0] * len(self._all_symptoms_list)
        symptom_name_to_index = {name: i for i, name in enumerate(self._all_symptoms_list)}
        for symptom in symptoms:
            symptom_name = symptom.name.strip()
            if symptom_name in symptom_name_to_index:
                index = symptom_name_to_index[symptom_name]
                weight = self._symptom_weights.get(symptom_name, 1.0)
                feature_vector[index] = 1.0 * weight
        return feature_vector

    def predict_specialties(self, symptoms: List[Symptom]) -> List[MedicalSpecialty]:
        if not symptoms:
            return []
        feature_vector = self._create_feature_vector(symptoms)
        predicted_specialties = self._model_repository.predict_specialties(feature_vector, self._predictions_to_return)
        return predicted_specialties

