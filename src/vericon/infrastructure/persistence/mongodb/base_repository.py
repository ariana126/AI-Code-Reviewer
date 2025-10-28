from abc import ABC, abstractmethod
from typing import Type

from ddd.domain.value import Identity
from underpy import JSON, Repository, Persistable

from vericon.infrastructure.persistence.mongodb.client import MongoDBClient


class MongoDBBaseRepository(Repository, ABC):
    def __init__(self, client: MongoDBClient):
        self._collection = client.get_collection(self.collection_name)

    @property
    @abstractmethod
    def collection_name(self) -> str:
        pass

    @property
    @abstractmethod
    def persistable_cls(self) -> Type[Persistable]:
        pass

    def find(self, id_: Identity) -> Persistable|None:
        data: JSON = self._collection.find_one({"id": id_.as_string()})
        if data is None:
            return None
        return self.persistable_cls.from_json(self.persistable_cls, data)

    def save(self, persistable: Persistable) -> None:
        self._collection.insert_one(persistable.to_json())