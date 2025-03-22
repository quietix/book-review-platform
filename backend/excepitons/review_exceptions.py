from . import (
    ItemDoesNotExist,
    CreateItemException,
    UpdateItemException,
    DeleteItemException
)


class ReviewDoesNotExist(ItemDoesNotExist):
    def get_detail(self):
        return "Review does not exist."


class CreateReviewException(CreateItemException):
    def get_detail(self):
        return "Failed to create the review."


class UpdateReviewException(UpdateItemException):
    def get_detail(self):
        return "Failed to update the review."


class DeleteReviewException(DeleteItemException):
    def get_detail(self):
        return "Failed to delete the review."
