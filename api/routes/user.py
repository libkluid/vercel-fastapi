from typing import Annotated
from fastapi import APIRouter, Depends
from api.entities import models, errors, response
from api.repositories import UserRepository, LicenseRepository
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
