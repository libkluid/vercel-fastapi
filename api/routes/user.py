from typing import Annotated
from fastapi import APIRouter, Depends
from api.entities import models
from api.repositories import UserRepository
from api.auth import verify_user


router = APIRouter(prefix="/user", tags=["user"])

@router.patch(
    path="/",
)
async def get_user(
    profile: models.UserProfile,
    user: Annotated[models.User, Depends(verify_user)],
    user_repository: Annotated[UserRepository, Depends(UserRepository)]
):
    user = await user_repository.update_profile(user, profile)
    return {
        "ok": True
    }
    
