from fastapi import FastAPI, HTTPException
from schema import (CreateTodoRequest, UpdateTodoRequest, CreateTodoResponse, UpdateTodoResponse,
                     GetTodoResponse, SearchTodoResponse, DeleteTodoResponse, LoginRequest, LoginResponse, CreateUserRequest, CreateUserResponse)
from lifespan import lifespan
from dapendancy import SessionDependency, TokenDependency
from constants import SUCCESS_RESPONSE
from sqlalchemy import select

import models
import crud
import datetime
from auth import hash_password, check_password


app = FastAPI(
    title='Todo API',
    description='Todo app',
    lifespan=lifespan 
)


@app.post('/api/v1/todo', tags=['todo'], response_model=CreateTodoResponse)
async def create_todo(todo: CreateTodoRequest, session: SessionDependency, token: TokenDependency):
    todo_dict = todo.model_dump(exclude_unset=True)
    todo_orm_obj = models.Todo(**todo_dict, user_id=token.user_id) 
    await crud.add_item(session, todo_orm_obj)
    return todo_orm_obj.dict

@app.get('/api/v1/todo/{todo_id}', tags=['todo'], response_model=GetTodoResponse)
async def get_todo(todo_id: int, session: SessionDependency, token: TokenDependency):
    todo_orm_obj = await crud.get_item_by_id(session, models.Todo, todo_id)
    if token.user.role == 'admin' or todo_orm_obj.user_id == token.user_id:
        return todo_orm_obj.dict
    raise HTTPException(403, 'Influent privileges')

@app.get('/api/v1/todo/', response_model=SearchTodoResponse)
async def search_todo(session: SessionDependency, title: str, important: bool = False):
    query = (
        select(models.Todo)
        .where(models.Todo.title == title, models.Todo.important == important)
        .limit(10000)
    )
    todos = await session.scalars(query)
    return {'results': [todo.dict for todo in todos]}

@app.patch('/api/v1/todo/{todo_id}', response_model=UpdateTodoResponse)
async def update_todo(todo_id: int, todo_data: UpdateTodoRequest, session: SessionDependency):
    todo_dict = todo_data.model_dump(exclude_unset=True)
    if todo_dict.get('done'):
        todo_dict['end_time'] = datetime.datetime.now()
    todo_orm_obj = await crud.get_item_by_id(session, models.Todo, todo_id)
    
    for field, value in todo_dict.items():
        setattr(todo_orm_obj, field, value)
    await crud.add_item(session, todo_orm_obj)    
    return SUCCESS_RESPONSE

@app.delete('/api/v1/todo/{todo_id}', response_model=DeleteTodoResponse)
async def delete_todo(todo_id: int, session: SessionDependency):
    todo_orm_obj = await crud.get_item_by_id(session, models.Todo, todo_id)
    await crud.delete_item(session, todo_orm_obj)
    return SUCCESS_RESPONSE

@app.post('/api/v1/user', tags=['user'], response_model=CreateUserResponse)
async def create_user(user_data: CreateUserRequest, session: SessionDependency):
    user_dict = user_data.model_dump(exclude_unset=True)
    user_dict['password'] = hash_password(user_dict['password'])
    user_orm_obj = models.User(**user_dict)
    await crud.add_item(session, user_orm_obj)
    # return CreateUserResponse(id=user_orm_obj.id, name=user_orm_obj.name, role=user_orm_obj.role)
    return user_orm_obj.dict 

@app.post('/api/v1/user/login', tags=['user'], response_model=LoginResponse)
async def login(login_data: LoginRequest, session: SessionDependency):
    query = select(models.User).where(models.User.name == login_data.name)
    user = await session.scalar(query)
    if user is None:
        raise HTTPException(401, 'Invalid credentials')
    if not check_password(login_data.password, user.password):
        raise HTTPException(401, 'Invalid credentials')
    token = models.Token(user_id=user.id)
    await crud.add_item(session, token)
    return token.dict



