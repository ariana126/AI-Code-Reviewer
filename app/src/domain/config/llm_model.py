from abc import ABC, abstractmethod
from typing import Any
from ddd.domain.value_object import ValueObject


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