import re
import unicodedata
from typing import List, Dict

from src.domain.models.symptom import Symptom
from src.domain.repositories.i_symptom_repository import ISymptomRepository

class SymptomMatcherService:

    def __init__(self, symptom_repository: ISymptomRepository):
        self._repository = symptom_repository
        self._variations_cache: Dict[str, List[str]] = {}

    def _load_variations_if_needed(self):
        if not self._variations_cache:
            self._variations_cache = self._repository.get_symptom_variations()

    @staticmethod
    def _normalize_text(text: str) -> str:
        if not text:
            return ""
        nfkd_form = unicodedata.normalize('NFD', text)
        normalized_text = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
        return normalized_text.lower()

    def find_matching_symptoms(self, text: str) -> List[Symptom]:
        self._load_variations_if_needed()
        found_symptoms = set()
        normalized_input_text = self._normalize_text(text)

        if not normalized_input_text:
            return []

        for canonical_symptom, variations in self._variations_cache.items():
            normalized_variations = [self._normalize_text(v) for v in variations if v]
            search_patterns = [self._normalize_text(canonical_symptom)] + normalized_variations
            escaped_patterns = [re.escape(p) for p in search_patterns if p]
            if not escaped_patterns:
                continue
            regex = r'\b(' + '|'.join(escaped_patterns) + r')\b'
            if re.search(regex, normalized_input_text):
                found_symptoms.add(canonical_symptom)
        return [Symptom(name=symptom_name) for symptom_name in found_symptoms]

