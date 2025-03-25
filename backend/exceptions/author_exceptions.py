from . import (
    ItemDoesNotExist,
    CreateItemException,
    UpdateItemException,
    DeleteItemException
)


class AuthorDoesNotExist(ItemDoesNotExist):
    def get_detail(self):
        return "Author does not exist."


class CreateAuthorException(CreateItemException):
    def get_detail(self):
        return "Failed to create the author."


class UpdateAuthorException(UpdateItemException):
    def get_detail(self):
        return "Failed to update the author."


class DeleteAuthorException(DeleteItemException):
    def get_detail(self):
        return "Failed to delete the author."
