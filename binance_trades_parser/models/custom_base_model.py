from pydantic import BaseModel


class CustomBaseModel(BaseModel):
    class Config:
        orm_mode = True
        underscore_attrs_are_private = True
