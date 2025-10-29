import dotenv
import pytest
from pydm import ServiceContainer

from vericon.infrastructure.boot import boot
from vericon.infrastructure.persistence.mongodb.client import MongoDBClient

dotenv.load_dotenv(".env.test", override=True)

@pytest.fixture(autouse=True)
def before_script():
    boot()
    mongodb_client: MongoDBClient = ServiceContainer.get_instance().get_service(MongoDBClient)
    mongodb_client.clear_all_collections()