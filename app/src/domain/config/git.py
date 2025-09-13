from abc import abstractmethod, ABC
from typing import Any
from ddd.domain.value_object import ValueObject


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
