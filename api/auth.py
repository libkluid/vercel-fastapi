from typing import Annotated
from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from api.repositories import UserRepository
from api.entities import models

bearer = HTTPBearer()

def authorization_credentails(
    credentials: Annotated[HTTPAuthorizationCredentials, Security(bearer)]
):
    token = credentials.credentials
    return token

async def verify_user(
        token: Annotated[str, Depends(authorization_credentails)],
        user_repository: Annotated[UserRepository, Depends(UserRepository)]
    ) -> models.User:
    user = await user_repository.get_user(token)
    return user
