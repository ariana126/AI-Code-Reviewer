# TODO: Separate classes
import copy
from abc import ABC, abstractmethod
from typing import Any
from ddd.domain.value_object import ValueObject
from ddd.framework.encapsulation import Encapsulated
from ddd.framework.mutability import Immutable

from app.src.infrastructure.n8n.sdk import N8nClient


class GitServer(ValueObject):
    __GIT_LAB: str = 'gitlab'
    __SUPPORTED_SERVERS: tuple[str] = (__GIT_LAB,)
    def __init__(self, name: str) -> None:
        if name not in self.__SUPPORTED_SERVERS:
            raise ValueError(f'"{name}" is not supported yet.')
        self.__name = name

    @classmethod
    def from_string(cls, name: str) -> 'GitServer':
        return cls(name)

    @property
    def name(self) -> str:
        return self.__name

class GitServerConfig(ABC):
    @abstractmethod
    def from_json(cls, data: dict[str, Any]) -> 'GitServerConfig':
        pass
    @abstractmethod
    def to_json(self) -> dict[str, Any]:
        pass

class GitlabConfig(GitServerConfig, ValueObject):
    __SERVER_KEY: str = 'server'
    __ACCESS_TOKEN_KEY: str = 'accessToken'
    __MERGE_REQUEST_ID_KEY: str = 'mergeRequestId'
    __PROJECT_OWNER_KEY: str = 'projectOwner'
    __PROJECT_NAME_KEY: str = 'projectName'

    def __init__(self, server: str, access_token: str, merge_request_id: str, project_owner: str, project_name: str) -> None:
        self.__server: str = server
        self.__access_token: str = access_token
        self.__merge_request_id: str = merge_request_id
        self.__project_owner: str = project_owner
        self.__project_name: str = project_name

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> 'GitlabConfig':
        if cls.__SERVER_KEY not in data:
            raise ValueError(f'"{cls.__SERVER_KEY}" is missing.')
        if cls.__ACCESS_TOKEN_KEY not in data:
            raise ValueError(f'"{cls.__ACCESS_TOKEN_KEY}" is missing.')
        if cls.__MERGE_REQUEST_ID_KEY not in data:
            raise ValueError(f'"{cls.__MERGE_REQUEST_ID_KEY}" is missing.')
        if cls.__PROJECT_OWNER_KEY not in data:
            raise ValueError(f'"{cls.__PROJECT_OWNER_KEY}" is missing.')
        if cls.__PROJECT_NAME_KEY not in data:
            raise ValueError(f'"{cls.__PROJECT_NAME_KEY}" is missing.')
        return cls(
            data[cls.__SERVER_KEY],
            data[cls.__ACCESS_TOKEN_KEY],
            data[cls.__MERGE_REQUEST_ID_KEY],
            data[cls.__PROJECT_OWNER_KEY],
            data[cls.__PROJECT_NAME_KEY]
        )

    def to_json(self) -> dict[str, Any]:
        return {
            self.__SERVER_KEY: self.__server,
            self.__ACCESS_TOKEN_KEY: self.__access_token,
            self.__MERGE_REQUEST_ID_KEY: self.__merge_request_id,
            self.__PROJECT_OWNER_KEY: self.__project_owner,
            self.__PROJECT_NAME_KEY: self.__project_name,
        }

class GitServerConfigFactory:
    @staticmethod
    def build(git_server: GitServer, data: dict[str, Any]) -> GitServerConfig:
        match git_server.name:
            case 'gitlab':
                return GitlabConfig.from_json(data)
            case _:
                raise ValueError(f'"{git_server.name}" is not supported yet.')


class LLMModelProvider(ValueObject):
    __OPEN_AI: str = 'openai'
    __SUPPORTED_PROVIDERS: tuple[str] = (__OPEN_AI,)
    def __init__(self, name: str) -> None:
        if name not in self.__SUPPORTED_PROVIDERS:
            raise ValueError(f'"{name}" is not supported yet.')
        self.__name = name
    @classmethod
    def from_string(cls, name: str) -> 'LLMModelProvider':
        return cls(name)
    @property
    def name(self) -> str:
        return self.__name

class LLMmodelProviderConfig(ABC):

    @abstractmethod
    def from_json(cls, data: dict[str, Any]) -> 'LLMmodelProviderConfig':
        pass
    @abstractmethod
    def to_json(self) -> dict[str, Any]:
        pass

class OpenAIConfig(LLMmodelProviderConfig, ValueObject):
    __API_KEY_KEY: str = 'apiKey'
    __BASE_URL_KEY: str = 'baseUrl'

    def __init__(self, api_key: str, base_url: str) -> None:
        self.__api_key: str = api_key
        self.__base_url: str = base_url

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> 'LLMmodelProviderConfig':
        if cls.__API_KEY_KEY not in data:
            raise ValueError(f'"{cls.__API_KEY_KEY}" is missing.')
        if cls.__BASE_URL_KEY not in data:
            raise ValueError(f'"{cls.__BASE_URL_KEY}" is missing.')
        return cls(data[cls.__API_KEY], data[cls.__BASE_URL_KEY])

    def to_json(self) -> dict[str, Any]:
        return {
            self.__API_KEY_KEY: self.__api_key,
            self.__BASE_URL_KEY: self.__base_url,
        }

class LLMModelProviderConfigFactory:
    @staticmethod
    def build(llm_model_provider: LLMModelProvider, data: dict[str, Any]) -> LLMmodelProviderConfig:
        match llm_model_provider.name:
            case 'openai':
                return OpenAIConfig.from_json(data)
            case _:
                raise ValueError(f'"{llm_model_provider.name}" is not supported.')


class Language(ValueObject):
    __PHP: str = 'php'
    __SUPPORTED_LANGUAGES: tuple[str] = (__PHP,)
    def __init__(self, name: str) -> None:
        if name not in self.__SUPPORTED_LANGUAGES:
            raise ValueError(f'"{name}" is not supported yet.')
        self.__name = name
    @classmethod
    def from_string(cls, name: str) -> 'Language':
        return cls(name)
    @property
    def name(self) -> str:
        return self.__name



# TODO: Create a DTO base class that extends Encapsulated, Immutable and facilitates logging (__str__ and __repr__)
class RequestReviewCommand(Encapsulated, Immutable):
    __GIT_SERVER_KEY: str = 'gitServer'
    __LLM_MODEL_PROVIDER_KEY: str = 'llmModelProvider'
    __LANGUAGE_KEY: str = 'language'
    __DEFAULT_BRANCH_KEY: str = 'defaultBranch'
    __MAX_ITERATIONS_KEY: str = 'maxIterations'
    __REVIEW_CHECKLISTS_KEY: str = 'reviewChecklists'
    __VERSION_KEY: str = 'version'

    def __init__(self, git_server: GitServer, git_server_config: GitServerConfig, llm_model_provider: LLMModelProvider, llm_model_provider_config: LLMmodelProviderConfig, language: Language, default_branch:str|None=None, max_iteration:int|None=None, review_checklist:str|None=None, version:str|None=None) -> None:
        self.__git_server = git_server
        self.__git_server_config = git_server_config
        self.__llm_model_provider = llm_model_provider
        self.__llm_model_provider_config = llm_model_provider_config
        self.__language = language
        self.__default_branch = default_branch
        self.__max_iterations = max_iteration
        self.__review_checklist = review_checklist
        self.__version = version

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

        if cls.__LANGUAGE_KEY not in request:
            raise ValueError(f'"{cls.__LANGUAGE_KEY}" is missing.')

        default_branch: str|None = None
        if request[cls.__DEFAULT_BRANCH_KEY] is not None:
            default_branch = request[cls.__DEFAULT_BRANCH_KEY]
        max_iterations: int|None= None
        if request[cls.__MAX_ITERATIONS_KEY] is not None:
            max_iterations = request[cls.__MAX_ITERATIONS_KEY]
        review_checklist: str|None = None
        if request[cls.__REVIEW_CHECKLISTS_KEY] is not None:
            review_checklist = request[cls.__REVIEW_CHECKLISTS_KEY]

        return cls(
            git_server,
            git_server_config,
            llm_model_provider,
            llm_model_provider_config,
            Language.from_string(request[cls.__LANGUAGE_KEY]),
            default_branch,
            max_iterations,
            review_checklist
        )

    def to_json(self) -> dict[str, Any]:
        return {
            self.__GIT_SERVER_KEY: self.__git_server.name,
            self.__git_server.name: self.__git_server_config.to_json(),
            self.__LLM_MODEL_PROVIDER_KEY: self.__llm_model_provider.name,
            self.__llm_model_provider.name: self.__llm_model_provider_config.to_json(),
            self.__LANGUAGE_KEY: self.__language.name,
            self.__DEFAULT_BRANCH_KEY: self.__default_branch,
            self.__MAX_ITERATIONS_KEY: self.__max_iterations,
            self.__REVIEW_CHECKLISTS_KEY: self.__review_checklist,
        }

    @property
    def version(self) -> str|None:
        return self.__version

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
        result: dict[str, Any] = self.__n8n_client.request_review(request.to_json(), request.version)
        return ReviewResult.from_json(result)