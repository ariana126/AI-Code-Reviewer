import pytest
from assertpy.assertpy import assert_that
from ddd.domain import AggregateRoot
from underpy import JSON
from pydm import ServiceContainer
from ddd.domain.value import Identity

from vericon.infrastructure.boot import boot
from vericon.infrastructure.persistence.mongodb.base_repository import MongoDBBaseRepository


class DummyPersistable(AggregateRoot):
    def __init__(self, id_: Identity, value: str):
        super().__init__(id_)
        self.value = value

    def to_json(self) -> JSON:
        return {
            'id': self._id.as_string(),
            'value': self.value
        }

    @staticmethod
    def from_json(cls, data: JSON) -> 'Persistable':
        return cls(Identity.from_string(data['id']), data['value'])


class ConcertedRepository(MongoDBBaseRepository):
    @property
    def collection_name(self) -> str:
        return "dummy-collection"

    @property
    def persistable_cls(self) -> type[DummyPersistable]:
        return DummyPersistable


def test_repository_retrieves_what_it_has_saved() -> None:
    # arrange
    boot()
    sut: ConcertedRepository = ServiceContainer.get_instance().get_service(ConcertedRepository)
    persistable: DummyPersistable = DummyPersistable(Identity('dummy-id'), 'dummy-value')
    sut.save(persistable)

    # act
    from_db = sut.find(persistable.id)

    # assert
    assert_that(from_db).is_not_none()
    assert_that(from_db).is_instance_of(DummyPersistable)
    assert_that(from_db.id).is_equal_to(persistable.id)
    assert_that(from_db.value).is_equal_to(persistable.value)

def test_repository_rais_error_if_it_is_requested_to_get_something_tha_has_not_saved() -> None:
    # arrange
    boot()
    sut: ConcertedRepository = ServiceContainer.get_instance().get_service(ConcertedRepository)

    # assert
    with pytest.raises(RuntimeError):
        # act
        sut.get(Identity('not-existed-id'))