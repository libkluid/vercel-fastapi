from typing import Annotated
from fastapi import APIRouter, Depends
from gotrue import AuthResponse
from api.entities import models
from api.repositories import UserRepository

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    path="/signin",
    summary="Sign in",
    description="Sign in with email and password",
)
async def sign_in(
    data: models.SignIn,
    user_repository: Annotated[UserRepository, Depends(UserRepository)]
) -> models.AuthToken:
    resp: AuthResponse = await user_repository.sign_in(data)
    return models.AuthToken(**resp.session.model_dump())

