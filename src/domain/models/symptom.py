from dataclasses import dataclass

@dataclass(frozen=True)
class Symptom:
    name: str
