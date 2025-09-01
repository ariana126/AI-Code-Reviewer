from typing import Any
import requests
from ddd.framework.encapsulation import Encapsulated
from ddd.framework.mutability import Immutable
from app.src.user_case.n8n_client import N8nClientInterface


class N8nSDK(Encapsulated, Immutable):
    # TODO: Implement authentication
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def post_webhook(self, path: str, body: dict[str, Any])->dict[str, Any]:
        response = requests.post(f"{self.base_url}/{path}", json=body)
        if response.status_code != requests.codes.ok:
            # TODO: Make custom error classes
            raise RuntimeError('Failed to post webhook', response.json())
        return response.json()

class N8nClient(N8nClientInterface, Encapsulated, Immutable):
    def __init__(self, sdk: N8nSDK, code_reviewer_webhook_path: str, default_version: str= 'v1'):
        self.sdk = sdk
        self.code_reviewer_webhook_path = code_reviewer_webhook_path
        self.default_version = default_version

    def request_review(self, data: dict[str, Any], version: str|None) -> dict[str, Any]:
        if version is None:
            version = self.default_version
        return self.sdk.post_webhook(f'{self.code_reviewer_webhook_path}/{version}', data)