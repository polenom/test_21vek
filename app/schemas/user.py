from typing import Optional

from pydantic import BaseModel


class UserResponseModel(BaseModel):
    id: int
    name: str
    dish_of_the_day: Optional[str]


class UserCreateModel(BaseModel):
    name: str
    dish_of_the_day: Optional[str] = None
