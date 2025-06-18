from abc import ABC, abstractmethod
from typing import List

from ..models.medical_specialty import MedicalSpecialty

class ISpecialtyPredictionModelRepository(ABC):
    """Interface for loading and interacting with the specialty prediction model."""

    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def predict_specialties(self, feature_vector: List[float], top_n: int) -> List[MedicalSpecialty]:
        pass

