from typing import Annotated
from fastapi import APIRouter, Depends
from gotrue import AuthResponse
from api.entities import models, errors
from api.repositories import UserRepository, LogRepository
from api.util import utcnow

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    path="/signin",
    summary="Sign in",
    description="Sign in with email and password",
)
async def sign_in(
    data: models.SignIn,
    user_repository: Annotated[UserRepository, Depends(UserRepository)],
    log_repository: Annotated[LogRepository, Depends(LogRepository)]
) -> models.AuthToken:
    resp: AuthResponse = await user_repository.sign_in(data)

    user: models.User = await user_repository.get_user(resp.session.access_token)
    if valid_until := user.user_metadata.get("valid_until"):
        if valid_until < utcnow():
            raise errors.UnauthorizedException()

    log = await log_repository.create_signin_log(user)

    return models.AuthToken(**resp.session.model_dump())

