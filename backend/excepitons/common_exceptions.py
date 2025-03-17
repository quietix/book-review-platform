from typing import Optional
from abc import abstractmethod

from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    def __init__(self,
                 status_code: Optional[int] = None,
                 detail: Optional[str] = None):
        d = detail or self.get_detail()
        status = status_code or self.get_status_code()
        super().__init__(status_code=status, detail=d)

    @abstractmethod
    def get_status_code(self):
        raise NotImplementedError()

    @abstractmethod
    def get_detail(self):
        raise NotImplementedError()


class ItemDoesNotExist(BaseHTTPException):
    def get_status_code(self):
        return 404

    def get_detail(self):
        return "Item does not exist."


class CreateItemException(BaseHTTPException):
    def get_status_code(self):
        return 400

    def get_detail(self):
        return "Failed to create the item."


class UpdateItemException(BaseHTTPException):
    def get_status_code(self):
        return 400

    def get_detail(self):
        return "Failed to update the item."


class DeleteItemException(BaseHTTPException):
    def get_status_code(self):
        return 400

    def get_detail(self):
        return "Failed to delete the item."
