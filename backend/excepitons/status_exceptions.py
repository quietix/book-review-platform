from . import (
    ItemDoesNotExist,
    CreateItemException,
    UpdateItemException,
    DeleteItemException
)


class StatusDoesNotExist(ItemDoesNotExist):
    def get_detail(self):
        return "Status does not exist."


class CreateStatusException(CreateItemException):
    def get_detail(self):
        return "Failed to create the status."


class UpdateStatusException(UpdateItemException):
    def get_detail(self):
        return "Failed to update the status."


class DeleteStatusException(DeleteItemException):
    def get_detail(self):
        return "Failed to delete the status."
