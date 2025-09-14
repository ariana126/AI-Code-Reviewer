from abc import ABC, abstractmethod
from app.src.domain.review.request import ReviewRequest
from app.src.domain.review.result import ReviewResult


class N8nClientInterface(ABC):
    @abstractmethod
    def request_review(self, request: ReviewRequest) -> ReviewResult:
        pass