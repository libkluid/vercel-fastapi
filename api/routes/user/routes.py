from typing import Annotated
from fastapi import APIRouter, Depends
from api.repository.user_repository import UserRepository, CreateUser
from api.service.uid import generate_uid

router = APIRouter(prefix="/user", tags=["user"])

@router.get('/uid/{uid}')
def get_user(
    uid: str,
    user_repository: Annotated[UserRepository, Depends(UserRepository)]
):
    user = user_repository.find_user_by_uid(uid)
    return user

@router.post('/')
def create_user(
    email: str,
    name: str,
    uid: Annotated[str, Depends(generate_uid)],
    user_repository: Annotated[UserRepository, Depends(UserRepository)]
):
    user = CreateUser(uid=uid, name=name, email=email)
    result = user_repository.create_user(user)
    print(result)
    return user
