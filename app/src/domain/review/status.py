from ddd.domain.value_object import ValueObject


class ReviewStatus(ValueObject):
    __CREATED: str = 'created'
    __COMPLETED: str = 'completed'
    __FAILED: str = 'failed'
    __VALID_STATUSES: tuple[str] = (__CREATED, __COMPLETED, __FAILED,)

    def __init__(self, status: str) -> None:
        if status not in self.__VALID_STATUSES:
            raise ValueError(f'Invalid review status: {status}')
        self.__status = status

    @classmethod
    def created(cls) -> 'ReviewStatus':
        return cls(cls.__CREATED)
    @classmethod
    def completed(cls) -> 'ReviewStatus':
        return cls(cls.__COMPLETED)
    @classmethod
    def failed(cls) -> 'ReviewStatus':
        return cls(cls.__FAILED)