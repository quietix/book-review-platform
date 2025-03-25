from typing import Optional

from fastapi import HTTPException


class ConfigurationError(HTTPException):
    default_detail = "Error in configuring server."
    default_status_code = 500

    def __init__(self,
                 status_code: Optional[int] = None,
                 detail: Optional[str] = None):
        status = status_code or self.default_status_code
        d = detail or self.default_detail
        super().__init__(status_code=status, detail=d)
