from pydantic import BaseModel, ConfigDict


class BaseStatus(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class StatusPreview(BaseStatus):
    id: int
    status: str


class StatusUpsert(BaseStatus):
    status: str
