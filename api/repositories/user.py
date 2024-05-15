from fastapi import Depends
from typing import Annotated
from supabase import AClient as Supabase
from gotrue import User, AuthResponse
from gotrue.errors import AuthApiError
from api.saas.supabase import async_client
from api.entities import errors, models

class UserRepository:
    supabase: Supabase

    def __init__(self, supabase: Annotated[Supabase, Depends(async_client)]):
        self.supabase = supabase

    async def sign_in(self, signin: models.SignIn) -> AuthResponse:
        try:
            resp = await self.supabase.auth.sign_in_with_password(
                credentials=signin.model_dump()
            )
            return resp
        except AuthApiError:
            raise errors.UnauthorizedException()

    async def update_profile(self, user: User, user_profile: models.UserProfile) -> User:
        await self.supabase.table("profiles").upsert({
            "id": user.id,
            "email": user.email,
            "name": user_profile.name,
        }).execute()

        profile = await self.get_profile(user)
        user.user_metadata = profile.model_dump()

        return user

    async def get_profile(self, user: User) -> models.UserProfile:
        resp = await self.supabase.table("profiles").select("*").eq("id", user.id).single().execute()
        return models.UserProfile.model_validate(resp.data)

    async def get_user(self, token: str) -> User:
        try:
            resp = await self.supabase.auth.get_user(token)
            user_profile = await self.get_profile(resp.user)

            user = resp.user
            user.user_metadata = user_profile.model_dump()

            return user
        except AuthApiError:
            raise errors.UnauthorizedException()

    async def find_uid(self, email: str) -> str:
        resp = await self.supabase.table("profiles").select("*").eq("email", email).single().execute()
        if not resp:
            raise errors.NotFoundException()

        return resp.data["id"]
