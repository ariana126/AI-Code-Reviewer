from ddd.framework.service import ServiceClass
from app.src.domain.review.result import ReviewResult
from app.src.domain.review.review import Review
from app.src.domain.review.service.n8n_client import N8nClientInterface


class Reviewer(ServiceClass):
    def __init__(self, n8n_client: N8nClientInterface):
        self.__n8n_client = n8n_client

    def start(self, review: Review) -> ReviewResult:
        try:
            result: ReviewResult = self.__n8n_client.request_review(review.data)
            review.complete_with(result)
            return result
        except Exception as error:
            # TODO: Capture error message
            review.failed_with('Review Failed.')
            raise error