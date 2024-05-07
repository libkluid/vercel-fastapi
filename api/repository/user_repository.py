from typing import Annotated
from fastapi import Depends
from supabase import Client
from pydantic import BaseModel
from api.adapter.supabase import supabase_client
from api.entity.models import User

class CreateUser(BaseModel):
    uid: str
    name: str
    email: str

class UserRepository:
    supabase: Client

    def __init__(
        self,
        supabase: Annotated[Client, Depends(supabase_client)]
    ) -> None:
        self.supabase = supabase

    def create_user(self, user: CreateUser) -> User:
        result = self.supabase.table("users").insert(user.model_dump()).execute()
        return User.model_validate(result.data[0])

    def find_user_by_uid(self, uid: str) -> User:
        result = self.supabase.table("users").select("*").eq("uid", uid).maybe_single().execute()
        if result:
            return User.model_validate(result.data)
        return result
