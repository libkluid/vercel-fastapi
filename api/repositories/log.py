import datetime
from typing import Union
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

    async def create_refresh_log(self, user: User) -> models.UserLog:
        signin_logs = await self.supabase.table("user_logs").insert({
            "uid": user.id,
            "email": user.email,
            "action": "refresh",
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

        result = license_registration_logs.data[0]
        return models.UserLog.model_validate(result)

    async def insert_action(self, user: User, service: str, name: str, action: Union[None, int, float, str, dict, list]):
        await self.supabase.table("user_actions").insert({
            "uid": user.id,
            "service": service,
            "email": user.email,
            "name": name,
            "data": action,
        }).execute()

    async def count_monthly_actions(self, user: User, service: str):
        now = datetime.datetime.now()
        last_month = now - datetime.timedelta(days=30)
        last_month = last_month.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        result = await self.supabase.table("user_actions").select("id").eq("uid", user.id).eq("service", service).gte("created_at", last_month).execute()
        return len(result.data)
