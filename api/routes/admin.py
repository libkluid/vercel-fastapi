from typing import Annotated
from fastapi import APIRouter, Depends
from gotrue import AuthResponse
from api.entities import models, errors
from api.repositories import UserRepository, LogRepository, LicenseRepository

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post(
    path="/user/services/{service}/grant",
    summary="allow user to access service",
    description="allow user to access service",
)
async def grant_user(
    service: str,
    data: models.GrantUser,
    user_repository: Annotated[UserRepository, Depends(UserRepository)],
    license_repository: Annotated[LicenseRepository, Depends(LicenseRepository)]
) -> models.License:
    uid = await user_repository.find_uid(data.email)

    license = await license_repository.find_license(uid, service)
    if not license:
        license = await license_repository.create_license(uid, data.email, service)
    else:
        license = await license_repository.update_license_key(uid, license, None)

    return license

@router.post(
    path="/user/services/{service}/expiration",
    summary="allow user to access service",
    description="allow user to access service",
)
async def update_expiration(
    service: str,
    data: models.UpdateExpiration,
    user_repository: Annotated[UserRepository, Depends(UserRepository)],
    license_repository: Annotated[LicenseRepository, Depends(LicenseRepository)]
) -> models.License:
    uid = await user_repository.find_uid(data.email)
    license = await license_repository.find_license(uid, service)
    if not license:
        raise errors.NotFoundException()
    else:
        license = await license_repository.update_license_expiration(uid, license, data.expires_at)

    return license
