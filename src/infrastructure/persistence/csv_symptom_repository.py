import pandas as pd
import os
import logging
from typing import List, Dict, Optional

from src.domain.repositories.i_symptom_repository import ISymptomRepository
from src.domain.models.symptom import Symptom

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CsvSymptomRepository(ISymptomRepository):

    def __init__(self, variations_path: str, weights_path: str):
        if not os.path.exists(variations_path):
            logger.error(f"Variations file not found at: {variations_path}")
            raise FileNotFoundError(f"Variations file not found: {variations_path}")
        if not os.path.exists(weights_path):
            logger.error(f"Weights file not found at: {weights_path}")
            raise FileNotFoundError(f"Weights file not found: {weights_path}")
            
        self._variations_path = variations_path
        self._weights_path = weights_path
        self._variations_cache: Optional[Dict[str, List[str]]] = None
        self._weights_cache: Optional[Dict[str, float]] = None
        self._all_symptoms_cache: Optional[List[str]] = None

    def _load_variations(self) -> Dict[str, List[str]]:
        try:
            df = pd.read_csv(self._variations_path)
            variations_dict = {}
            if 'referencia' not in df.columns:
                logger.error(f"'referencia' column not found in {self._variations_path}")
                return {}
                 
            for _, row in df.iterrows():
                canonical = row["referencia"]
                if pd.isna(canonical):
                    continue
                variations = row.drop("referencia").dropna().astype(str).tolist()
                variations_dict[str(canonical)] = variations
            logger.info(f"Successfully loaded variations from {self._variations_path}")
            return variations_dict
        except Exception as e:
            logger.error(f"Error loading variations from {self._variations_path}: {e}", exc_info=True)
            return {}

    def _load_weights(self) -> Dict[str, float]:
        try:
            df = pd.read_csv(self._weights_path)
            if 'Sintoma' not in df.columns or 'Peso' not in df.columns:
                logger.error(f"Required columns (\"Sintoma\", \"Peso\") not found in {self._weights_path}")
                return {}
            df["Peso"] = pd.to_numeric(df["Peso"], errors="coerce")
            df = df.dropna(subset=["Sintoma", "Peso"])
            
            weights_dict = dict(zip(df["Sintoma"].astype(str).str.strip(), df["Peso"]))
            logger.info(f"Successfully loaded weights from {self._weights_path}")
            return weights_dict
        except Exception as e:
            logger.error(f"Error loading weights from {self._weights_path}: {e}", exc_info=True)
            return {}

    def get_symptom_variations(self) -> Dict[str, List[str]]:
        """Loads and returns a dictionary mapping canonical symptom names to their variations."""
        if self._variations_cache is None:
            self._variations_cache = self._load_variations()
        return self._variations_cache.copy()

    def get_symptom_weights(self) -> Dict[str, float]:
        """Loads and returns a dictionary mapping symptom names to their weights."""
        if self._weights_cache is None:
            self._weights_cache = self._load_weights()
        return self._weights_cache.copy()
        
    def get_all_symptom_names(self) -> List[str]:
        """Loads and returns a list of all known canonical symptom names from the weights file."""
        if self._all_symptoms_cache is None:
            weights = self.get_symptom_weights()
            self._all_symptoms_cache = sorted(list(weights.keys()))
        return self._all_symptoms_cache.copy()


