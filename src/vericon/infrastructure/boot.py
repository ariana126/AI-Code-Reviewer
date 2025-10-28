from dotenv import load_dotenv
from pydm import ServiceContainer, EnvParametersBag

from vericon.infrastructure.persistence.mongodb.client import MongoDBClient


def boot() -> None:
    service_container: ServiceContainer = ServiceContainer.get_instance()

    load_dotenv()
    service_container.set_parameters(EnvParametersBag())

    service_container.bind_parameters(MongoDBClient, {
        'connection_string': 'MONGODB_CONNECTION_STRING',
        'database_name': 'MONGODB_DATABASE',
    })