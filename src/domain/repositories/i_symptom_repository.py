from abc import ABC, abstractmethod
from typing import List, Dict, Optional

from ..models.symptom import Symptom

class ISymptomRepository(ABC):

    @abstractmethod
    def get_symptom_variations(self) -> Dict[str, List[str]]:
        pass

    @abstractmethod
    def get_symptom_weights(self) -> Dict[str, float]:
        pass

    @abstractmethod
    def get_all_symptom_names(self) -> List[str]:
        pass

