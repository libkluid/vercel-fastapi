from typing import Annotated
from fastapi import APIRouter, Depends
from gotrue import AuthResponse
from api.entities import models, errors
from api.repositories import UserRepository, LogRepository, LicenseRepository
from api.util import utcnow

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post(
    path="/user/grant",
    summary="allow user to access service",
    description="allow user to access service",
)
async def grant_user(
    data: models.GrantUser,
    user_repository: Annotated[UserRepository, Depends(UserRepository)],
    license_repository: Annotated[LicenseRepository, Depends(LicenseRepository)]
):
    uid = await user_repository.find_uid(data.email)

    license = await license_repository.find_license(uid, data.service)
    if not license:
        await license_repository.create_license(uid, data.service)
    else:
        await license_repository.update_license_key(uid, license, None)

    return {
        "ok": True,
    }

