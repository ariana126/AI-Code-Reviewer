from abc import ABC, abstractmethod
from typing import Any


class N8nClientInterface(ABC):
    @abstractmethod
    def request_review(self, data: dict[str, Any], version: str|None) -> dict[str, Any]:
        pass