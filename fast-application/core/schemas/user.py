from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserUpdate(UserBase):
    username: str | None = None
    foo: int | None = None
    bar: int | None = None
