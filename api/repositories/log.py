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
            "data": None,
        }).execute()

        return models.UserLog.model_validate(signin_logs.data[0])