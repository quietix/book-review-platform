from . import (
    ItemDoesNotExist,
    CreateItemException,
    UpdateItemException,
    DeleteItemException
)


class GenreDoesNotExist(ItemDoesNotExist):
    def get_detail(self):
        return "Genre does not exist."


class CreateGenreException(CreateItemException):
    def get_detail(self):
        return "Failed to create the genre."


class UpdateGenreException(UpdateItemException):
    def get_detail(self):
        return "Failed to update the genre."


class DeleteGenreException(DeleteItemException):
    def get_detail(self):
        return "Failed to delete the genre."
