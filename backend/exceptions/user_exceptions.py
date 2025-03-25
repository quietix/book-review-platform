from . import (
    ItemDoesNotExist,
    CreateItemException,
    UpdateItemException,
    DeleteItemException
)


class UserDoesNotExist(ItemDoesNotExist):
    def get_detail(self):
        return "User does not exist."


class CreateUserException(CreateItemException):
    def get_detail(self):
        return "Failed to create the user."


class UpdateUserException(UpdateItemException):
    def get_detail(self):
        return "Failed to update the user."


class DeleteUserException(DeleteItemException):
    def get_detail(self):
        return "Failed to delete the user."
