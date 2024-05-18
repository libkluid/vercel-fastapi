from fastapi import Depends
from typing import Annotated
from supabase import AClient as Supabase
from gotrue import User
from api.saas.supabase import async_client
from api.entities import models

class LogRepository:
    supabase: Supabase

    def __init__(self, supabase: Annotated[Supabase, Depends(async_client)]):
        self.supabase = supabase

    async def create_signin_log(self, user: User) -> models.UserLog:
        signin_logs = await self.supabase.table("user_logs").insert({
            "uid": user.id,
            "email": user.email,
            "action": "signin",
        }).execute()

        return models.UserLog.model_validate(signin_logs.data[0])

    async def create_update_profile_log(self, user: User, profile: models.UserProfile) -> models.UserLog:
        update_profile_logs = await self.supabase.table("user_logs").insert({
            "uid": user.id,
            "email": user.email,
            "action": "update_profile",
            "data": profile.model_dump(),
        }).execute()

        return models.UserLog.model_validate(update_profile_logs.data[0])

    async def create_license_registration(self, user: User, license: models.License, license_key: str) -> models.UserLog:
        license_registration_logs = await self.supabase.table("user_logs").insert({
            "uid": user.id,
            "email": user.email,
            "action": "license_registration",
            "data": {
                "service": license.service,
                "license_key": license_key,
            },
        }).execute()

        return models.UserLog.model_validate(license_registration_logs.data[0])
