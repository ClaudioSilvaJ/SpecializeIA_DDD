import pickle
import numpy as np
import os
import logging
from typing import List, Any

from src.domain.repositories.i_specialty_prediction_model_repository import ISpecialtyPredictionModelRepository
from src.domain.models.medical_specialty import MedicalSpecialty
from src.domain.models.symptom import Symptom

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
class PklSpecialtyPredictionModelRepository(ISpecialtyPredictionModelRepository):

    def __init__(self, model_path: str):
        if not os.path.exists(model_path):
            logger.error(f"Model file not found at: {model_path}")
            raise FileNotFoundError(f"Model file not found: {model_path}")
            
        self._model_path = model_path
        self._model: Any = None

    def load_model(self):
        """Loads the prediction model from the .pkl file."""
        if self._model is None:
            try:
                with open(self._model_path, 'rb') as file:
                    self._model = pickle.load(file)
                logger.info(f"Successfully loaded prediction model from {self._model_path}")
            except Exception as e:
                logger.error(f"Error loading model from {self._model_path}: {e}", exc_info=True)
                raise RuntimeError(f"Failed to load prediction model: {e}")

    def predict_specialties(self, feature_vector: List[float], top_n: int) -> List[MedicalSpecialty]:
        """Predicts the top N medical specialties based on the feature vector."""
        if self._model is None:
            logger.error("Prediction model is not loaded. Call load_model() first.")
            raise RuntimeError("Prediction model not loaded.")
            
        if not feature_vector:
            logger.warning("Received empty feature vector for prediction.")
            return []

        try:
            feature_array = np.array(feature_vector).reshape(1, -1)
            predictions_proba = self._model.predict_proba(feature_array)

            top_indices = np.argsort(predictions_proba[0])[-top_n:][::-1]
            all_classes = self._model.classes_
            top_specialties = [all_classes[i] for i in top_indices]
            
            logger.info(f"Predicted specialties: {top_specialties}")
            return [MedicalSpecialty(name=str(specialty)) for specialty in top_specialties]
            
        except Exception as e:
            logger.error(f"Error during specialty prediction: {e}", exc_info=True)
            return []

