from typing import Annotated
from fastapi import APIRouter, Depends
from api.entities import models, errors, response
from api.repositories import UserRepository, LicenseRepository, LogRepository
from api.auth import verify_user


router = APIRouter(prefix="/user", tags=["user"])

@router.get(
    path="",
    summary="Get user profile",
    description="Get user profile",
)
async def get_user(
    user: Annotated[models.User, Depends(verify_user)],
    user_repository: Annotated[UserRepository, Depends(UserRepository)]
) -> response.UserProfileResponse:
    profile = await user_repository.get_profile(user)
    return response.UserProfileResponse.model_validate(profile)

@router.get(
    path="/services/{service}",
    summary="Get user service",
    description="Get user service",
)
async def get_user_services(
    service: str,
    user: Annotated[models.User, Depends(verify_user)],
    license_repository: Annotated[LicenseRepository, Depends(LicenseRepository)]
) -> response.UserLicenseResponse:
    license: models.License = await license_repository.find_license(user.id, service)
    if not license:
        raise errors.NotFoundException()
    return license 

@router.post(
    path="/services/{service}/action",
    summary="Makes a user action",
    description="Makes a user action",
)
async def make_user_action(
    service: str,
    data: models.Action,
    user: Annotated[models.User, Depends(verify_user)],
    user_repository: Annotated[UserRepository, Depends(UserRepository)],
    log_repository: Annotated[LogRepository, Depends(LogRepository)],
    license_repository: Annotated[LicenseRepository, Depends(LicenseRepository)]
):
    profile = await user_repository.get_profile(user)
    action_count = await log_repository.count_monthly_actions(user, service)
    license: models.License = await license_repository.find_license(user.id, service)
    if not license:
        raise errors.UnauthorizedException()
    if action_count > license.monthly_action_limit:
        raise errors.TooManyRequestsException()

    await log_repository.insert_action(user, service, profile.name, data.data)

    return {
        "ok": True,
    }
