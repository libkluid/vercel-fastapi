from fastapi import Depends
from typing import Annotated
from supabase import AClient as Supabase
from gotrue import User
from api.saas.supabase import async_client
from api.entities import models

class LicenseRepository:
    supabase: Supabase

    def __init__(self, supabase: Annotated[Supabase, Depends(async_client)]):
        self.supabase = supabase

    async def find_license(self, user: User, service: str) -> models.License | None:
        resp = await self.supabase.table("user_licenses").select("*").eq("uid", user.id).eq("service", service).maybe_single().execute()

        if not resp:
            return None

        return models.License.model_validate(resp.data) 

    async def update_license_key(self, user: User, license: models.License, license_key: str):
        await self.supabase.table("user_licenses").upsert({
            "id": license.id,
            "uid": user.id,
            "service": license.service,
            "license_key": license_key,
        }).execute()
