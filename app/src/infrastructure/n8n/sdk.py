from typing import Any
import requests
from ddd.framework.encapsulation import Encapsulated
from ddd.framework.mutability import Immutable
from app.src.user_case.n8n_client import N8nClientInterface


class N8nSDK(Encapsulated, Immutable):
    # TODO: Implement authentication
    def __init__(self, base_url: str) -> None:
        self.__base_url = base_url

    def post_webhook(self, path: str, body: dict[str, Any])->dict[str, Any]:
        response = requests.post(f"{self.__base_url}/{path}", json=body)
        if response.status_code != requests.codes.ok:
            # TODO: Make custom error classes
            raise RuntimeError('N8n Failed.', response.json())
        return response.json()

class N8nClient(N8nClientInterface, Encapsulated, Immutable):
    def __init__(self, sdk: N8nSDK, code_reviewer_webhook_path: str):
        self.__sdk = sdk
        self.__code_reviewer_webhook_path = code_reviewer_webhook_path

    # TODO: Make response classes
    def request_review(self, data: dict[str, Any]) -> dict[str, Any]:
        return self.__sdk.post_webhook(self.__code_reviewer_webhook_path, data)