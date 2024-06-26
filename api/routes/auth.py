import datetime
from typing import Annotated
from fastapi import APIRouter, Depends
from gotrue import AuthResponse
from api.entities import models, errors
from api.repositories import UserRepository, LogRepository, LicenseRepository

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    path="/signin",
    summary="Sign in",
    description="Sign in with email and password",
)
async def sign_in(
    data: models.SignIn,
    user_repository: Annotated[UserRepository, Depends(UserRepository)],
    log_repository: Annotated[LogRepository, Depends(LogRepository)],
    license_repository: Annotated[LicenseRepository, Depends(LicenseRepository)]
) -> models.AuthToken:
    resp: AuthResponse = await user_repository.sign_in(data)
    user: models.User = await user_repository.get_user(resp.session.access_token)
    license: models.License = await license_repository.find_license(user.id, data.service)

    utcnow = datetime.datetime.now(datetime.timezone.utc)

    if not license:
        raise errors.UnauthorizedException()
    if not license.license_key:
        await license_repository.update_license_key(user.id, license, data.service_key)
        await log_repository.create_license_registration(user, license, data.service_key)
    elif license.license_key != data.service_key:
        raise errors.UnauthorizedException()
    elif license.expires_at is not None and license.expires_at < utcnow:
        raise errors.UnauthorizedException()

    log = await log_repository.create_signin_log(user)

    return models.AuthToken(**resp.session.model_dump())

@router.post(
    path="/signup",
    summary="sign up",
    description="sign up",
)
async def sign_up(
    data: models.SignUp,
    user_repository: Annotated[UserRepository, Depends(UserRepository)],
):
    await user_repository.sign_up(data.email, data.password)
    return {
        "ok": True,
    }

@router.post(
    path="/refresh",
    summary="Refresh",
    description="Refresh access token",
)
async def refresh(
    data: models.Refresh,
    user_repository: Annotated[UserRepository, Depends(UserRepository)],
    license_repository: Annotated[LicenseRepository, Depends(LicenseRepository)]
) -> models.AuthToken:
    resp: AuthResponse = await user_repository.refresh(data)
    user: models.User = await user_repository.get_user(resp.session.access_token)
    license: models.License = await license_repository.find_license(user.id, data.service)

    utcnow = datetime.datetime.now(datetime.timezone.utc)

    if not license:
        raise errors.UnauthorizedException()
    elif license.expires_at is not None and license.expires_at < utcnow:
        raise errors.UnauthorizedException()

    return models.AuthToken(**resp.session.model_dump())
