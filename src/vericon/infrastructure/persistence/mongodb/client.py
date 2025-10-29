from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from underpy import Immutable, Encapsulated

class MongoDBClient(Encapsulated, Immutable):
    def __init__(self, connection_string: str, database_name: str) -> None:
        self.__client: MongoClient = MongoClient(connection_string)
        self.__db: Database = self.__client[database_name]

    def get_collection(self, name: str) -> Collection:
        return self.__db[name]

    def clear_all_collections(self) -> None:
        for name in self.__db.list_collection_names():
            self.__db[name].delete_many({})