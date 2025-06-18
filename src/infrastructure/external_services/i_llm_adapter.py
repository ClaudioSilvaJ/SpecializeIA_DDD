from abc import ABC, abstractmethod

class ILLMAdapter(ABC):

    @abstractmethod
    async def extract_symptoms_from_message(self, message: str) -> str:
        pass

