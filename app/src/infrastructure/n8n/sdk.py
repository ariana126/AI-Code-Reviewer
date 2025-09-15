from typing import Any
import requests
from underpy import ServiceClass
from app.src.domain.review.request import ReviewRequest
from app.src.domain.review.result import ReviewResult
from app.src.domain.review.service.n8n_client import N8nClientInterface


class N8nSDK(ServiceClass):
    # TODO: Implement authentication
    def __init__(self, base_url: str) -> None:
        self.__base_url = base_url

    def post_webhook(self, path: str, body: dict[str, Any])->dict[str, Any]:
        response = requests.post(f"{self.__base_url}/{path}", json=body)
        if response.status_code != requests.codes.ok:
            # TODO: Make custom error classes
            raise RuntimeError('N8n Failed.', response.json())
        return response.json()

class N8nClient(N8nClientInterface, ServiceClass):
    def __init__(self, sdk: N8nSDK, code_reviewer_webhook_path: str):
        self.__sdk = sdk
        self.__code_reviewer_webhook_path = code_reviewer_webhook_path

    def request_review(self, request: ReviewRequest) -> ReviewResult:
        n8n_response = self.__sdk.post_webhook(self.__code_reviewer_webhook_path, request.to_json())
        return ReviewResult.from_json(n8n_response)