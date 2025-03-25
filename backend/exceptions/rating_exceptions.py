from . import (
    ItemDoesNotExist,
    CreateItemException,
    UpdateItemException,
    DeleteItemException
)


class RatingDoesNotExist(ItemDoesNotExist):
    def get_detail(self):
        return "Rating does not exist."


class CreateRatingException(CreateItemException):
    def get_detail(self):
        return "Failed to create the rating."


class UpdateRatingException(UpdateItemException):
    def get_detail(self):
        return "Failed to update the rating."


class DeleteRatingException(DeleteItemException):
    def get_detail(self):
        return "Failed to delete the rating."
