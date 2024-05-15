from typing import Any, Union
from datetime import datetime
from gotrue import User
from pydantic import BaseModel, Json

class SignIn(BaseModel):
    email: str
    password: str
    service: str
    service_key: str

class AuthToken(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str

class UserProfile(BaseModel):
    name: str

class UserLog(BaseModel):
    uid: str
    email: str
    action: str
    data: Union[Json[Any], None]

class License(BaseModel):
    id: int
    uid: str
    service: str
    license_key: Union[str, None]
    expires_at: Union[datetime, None]

class GrantUser(BaseModel):
    email: str
    service: str

__all__ = [
    "User",
    "SignIn",
    "AuthToken",
    "UserLog",
    "License",
    "GrantUser",
]
