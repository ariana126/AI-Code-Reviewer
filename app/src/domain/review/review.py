from ddd.domain.aggregate_root import AggregateRoot
from ddd.domain.value.identity import Identity
from app.src.domain.review.request import ReviewRequest
from app.src.domain.review.result import ReviewResult
from app.src.domain.review.status import ReviewStatus


class Review(AggregateRoot):
    def __init__(self, id_: Identity, status: ReviewStatus, request: ReviewRequest, result: ReviewResult|None = None, error: str|None = None):
        if result is not None and error is not None:
            raise ValueError(f'result and error are mutually exclusive. review id: {id_}')
        super().__init__(id_)
        self.__status = status
        self.__request = request
        self.__result = result
        self.__error = error

    @property
    def data(self) -> ReviewRequest:
        return self.__request

    def is_completed(self) -> bool:
        return ReviewStatus.completed().equals(self.__status)

    def complete_with(self, result: ReviewResult) -> None:
        self.__result = result
        self.__error = None
        self.__status = ReviewStatus.completed()
        # TODO: Capture domain event

    def failed_with(self, error: str) -> None:
        if self.is_completed():
            raise ValueError(f'Review has already completed. id: {self.id_}')
        self.__error = error
        self.__status = ReviewStatus.failed()
        # TODO: Capture domain event