from fastapi import HTTPException


class ItemDoesNotExist(HTTPException):
    def __init__(self):
        detail = self.generate_detail()
        super().__init__(status_code=404, detail=detail)

    def generate_detail(self):
        return "Item does not exist."


class UserDoesNotExist(ItemDoesNotExist):
    def generate_detail(self):
        return "User does not exist."
