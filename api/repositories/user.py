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

    async def get_user(self, token: str) -> User:
        try:
            resp = await self.supabase.auth.get_user(token)
            return resp.user
        except AuthApiError:
            raise errors.UnauthorizedException()
