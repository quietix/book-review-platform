from . import (
    ItemDoesNotExist,
    CreateItemException,
    UpdateItemException,
    DeleteItemException
)


class BookDoesNotExist(ItemDoesNotExist):
    def get_detail(self):
        return "Book does not exist."


class CreateBookException(CreateItemException):
    def get_detail(self):
        return "Failed to create the book."


class UpdateBookException(UpdateItemException):
    def get_detail(self):
        return "Failed to update the book."


class DeleteBookException(DeleteItemException):
    def get_detail(self):
        return "Failed to delete the book."
