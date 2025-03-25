from .base_exceptions import BaseHTTPException


class IsbnAPIException(BaseHTTPException):
    def get_status_code(self):
        return 500

    def get_detail(self):
        return "Unexpected error from the ISBN API."
