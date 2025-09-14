import copy
from typing import Any
from ddd.domain.value_object import ValueObject


class ReviewResult(ValueObject):
    def __init__(self, issues: dict[str, list[dict[str, Any]]]) -> None:
        self.__issues = issues
    @classmethod
    def from_json(cls, data: dict[str, Any]) -> 'ReviewResult':
        return cls(data['issues'])
    @property
    def issues(self) -> dict[str, Any]:
        return copy.deepcopy(self.__issues)