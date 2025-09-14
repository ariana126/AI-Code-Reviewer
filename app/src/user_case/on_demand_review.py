from typing import Any
from ddd.domain.value.identity import Identity
from ddd.application.command import Command
from ddd.application.command_handler import CommandHandler
from app.src.domain.review.request import ReviewRequest
from app.src.domain.review.review import Review
from app.src.domain.review.service.reviewer import Reviewer
from app.src.domain.review.status import ReviewStatus


class ReviewOnDemandCommand(Command):
    def __init__(self, request: ReviewRequest):
        self.__request = request
    @property
    def data(self) -> ReviewRequest:
        return self.__request
    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> 'ReviewOnDemandCommand':
        return ReviewOnDemandCommand(ReviewRequest.from_json(json_data))

class ReviewOnDemandCommandHandler(CommandHandler):
    def __init__(self, reviewer: Reviewer):
        self.__reviewer = reviewer

    def execute(self, command: ReviewOnDemandCommand) -> dict[str, Any]:
        review: Review = Review(Identity.from_string('on-demand'), ReviewStatus.created(), command.data)
        return self.__reviewer.start(review).to_json()