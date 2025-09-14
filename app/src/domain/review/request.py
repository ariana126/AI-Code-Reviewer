from typing import Any
from ddd.domain.value_object import ValueObject
from app.src.domain.config.git import GitServer, GitServerConfig, GitServerConfigFactory
from app.src.domain.config.llm_model import LLMmodelProviderConfig, LLMModelProvider, LLMModelProviderConfigFactory


class ReviewRequest(ValueObject):
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
    def from_json(cls, request: dict[str, Any]) -> 'ReviewRequest':
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