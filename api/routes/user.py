from typing import Annotated
from fastapi import APIRouter, Depends
from api.entities import models
from api.repositories import UserRepository
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
) -> models.UserProfile:
    profile = await user_repository.get_profile(user)
    return profile

@router.patch(
    path="",
    summary="Update user profile",
    description="Update user profile",
)
async def update_user(
    profile: models.UserProfile,
    user: Annotated[models.User, Depends(verify_user)],
    user_repository: Annotated[UserRepository, Depends(UserRepository)]
):
    user = await user_repository.update_profile(user, profile)
    return {
        "ok": True
    }
    
