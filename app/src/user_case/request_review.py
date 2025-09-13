import copy
from typing import Any
from ddd.framework.encapsulation import Encapsulated
from ddd.framework.mutability import Immutable
from app.src.domain.config.git import GitServer, GitServerConfig, GitServerConfigFactory
from app.src.domain.config.llm_model import LLMModelProvider, LLMmodelProviderConfig, LLMModelProviderConfigFactory
from app.src.infrastructure.n8n.sdk import N8nClient

# TODO: Create a DTO base class that extends Encapsulated, Immutable and facilitates logging (__str__ and __repr__)
class RequestReviewCommand(Encapsulated, Immutable):
    __GIT_SERVER_KEY: str = 'gitServer'
    __LLM_MODEL_PROVIDER_KEY: str = 'llmModelProvider'
    __DEFAULT_BRANCH_KEY: str = 'defaultBranch'
    __MAX_ITERATIONS_KEY: str = 'maxIterations'

    def __init__(self, git_server: GitServer, git_server_config: GitServerConfig, llm_model_provider: LLMModelProvider, llm_model_provider_config: LLMmodelProviderConfig, default_branch: str, max_iterations: int) -> None:
        self.__git_server = git_server
        self.__git_server_config = git_server_config
        self.__llm_model_provider = llm_model_provider
        self.__llm_model_provider_config = llm_model_provider_config
        self.__default_branch = default_branch
        self.__max_iterations = max_iterations

    @classmethod
    def from_request(cls, request: dict[str, Any])->'RequestReviewCommand':
        if cls.__GIT_SERVER_KEY not in request:
            raise ValueError(f'"{cls.__GIT_SERVER_KEY}" is missing.')
        git_server: GitServer = GitServer.from_string(request[cls.__GIT_SERVER_KEY])
        if git_server.name not in request:
            raise ValueError(f'"{git_server.name}" is missing.')
        git_server_config: GitServerConfig = GitServerConfigFactory.build(git_server, request[git_server.name])

        if cls.__LLM_MODEL_PROVIDER_KEY not in request:
            raise ValueError(f'"{cls.__LLM_MODEL_PROVIDER_KEY}" is missing.')
        llm_model_provider: LLMModelProvider = LLMModelProvider.from_string(request[cls.__LLM_MODEL_PROVIDER_KEY])
        if llm_model_provider.name not in request:
            raise ValueError(f'"{llm_model_provider.name}" is missing.')
        llm_model_provider_config = LLMModelProviderConfigFactory.build(llm_model_provider, request[llm_model_provider.name])

        default_branch: str = 'develop'
        if request[cls.__DEFAULT_BRANCH_KEY] is not None:
            default_branch = request[cls.__DEFAULT_BRANCH_KEY]
        max_iterations: int = 10
        if request[cls.__MAX_ITERATIONS_KEY] is not None:
            max_iterations = request[cls.__MAX_ITERATIONS_KEY]

        return cls(
            git_server,
            git_server_config,
            llm_model_provider,
            llm_model_provider_config,
            default_branch,
            max_iterations
        )

    def to_json(self) -> dict[str, Any]:
        return {
            self.__GIT_SERVER_KEY: self.__git_server.name,
            self.__git_server.name: self.__git_server_config.to_json(),
            self.__LLM_MODEL_PROVIDER_KEY: self.__llm_model_provider.name,
            self.__llm_model_provider.name: self.__llm_model_provider_config.to_json(),
            self.__DEFAULT_BRANCH_KEY: self.__default_branch,
            self.__MAX_ITERATIONS_KEY: self.__max_iterations,
        }

class ReviewResult(Encapsulated, Immutable):
    def __init__(self, data: dict[str, Any]) -> None:
        self.__data = data
    @classmethod
    def from_json(cls, data: dict[str, Any]) -> 'ReviewResult':
        return cls(data)
    @property
    def data(self) -> dict[str, Any]:
        return copy.deepcopy(self.__data)

class RequestReviewCommandHandler(Encapsulated, Immutable):
    def __init__(self, n8n_client: N8nClient):
        self.__n8n_client = n8n_client

    def execute(self, request: RequestReviewCommand)->ReviewResult:
        result: dict[str, Any] = self.__n8n_client.request_review(request.to_json())
        # TODO: Make response classes in n8n
        return ReviewResult.from_json(result)