from typing import Literal
import datetime
import uuid
from pydantic import BaseModel


class SuccessResponse(BaseModel):
    status: Literal['success']


class CreateTodoRequest(BaseModel):
    title: str
    important: bool | None = False

class UpdateTodoRequest(BaseModel):
    title: str | None = None
    important: bool | None = None
    done: bool | None = None

class CreateTodoResponse(BaseModel):
    id: int
    title: str
    important: bool
    done: bool
    start_time: str
    end_time: str | None = None

class UpdateTodoResponse(SuccessResponse):
    pass

class GetTodoResponse(BaseModel):
    id: int
    title: str
    important: bool
    done: bool
    start_time: datetime.datetime
    end_time: datetime.datetime | None

class SearchTodoResponse(BaseModel):
    results: list[GetTodoResponse]

class DeleteTodoResponse(SuccessResponse):
    pass

class BaseUserRequest(BaseModel):
    name: str
    password: str

class LoginRequest(BaseUserRequest):
    pass

class LoginResponse(BaseModel):
    token: uuid.UUID

class CreateUserRequest(BaseUserRequest):
    pass

class CreateUserResponse(BaseModel):
    id: int
    name: str
    role: str
