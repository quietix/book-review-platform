from . import (
    ItemDoesNotExist,
    CreateItemException,
    DeleteItemException
)


class ReadingItemDoesNotExist(ItemDoesNotExist):
    def get_detail(self):
        return "Reading Item does not exist."


class CreateReadingItemException(CreateItemException):
    def get_detail(self):
        return "Failed to create the Reading Item."


class DeleteReadingItemException(DeleteItemException):
    def get_detail(self):
        return "Failed to delete the Reading Item."
