from fastapi import APIRouter

from database import create_user, delete_user, get_user, get_users, update_user
from models.user import User

routes_user = APIRouter()


@routes_user.post('/create', response_model=User)
def create(user: User):
    return create_user(user.dict())


@routes_user.get('/get/{id}')
def get_by_id(id: str):
    return get_user(id)


@routes_user.get('/all')
def get_all_users():
    return get_users()


@routes_user.post('/delete')
def delete_user(user: User):
    return delete_user(user.dict())


@routes_user.post('/update')
def update(user: User):
    return update_user(user.dict())
