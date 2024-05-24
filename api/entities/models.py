from typing import Union
from datetime import datetime
from gotrue import User
from pydantic import BaseModel

class SignIn(BaseModel):
    email: str
    password: str
    service: str
    service_key: str

class Refresh(BaseModel):
    token: str
    service: str

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
    data: Union[None, int, float, str, dict, list]

class License(BaseModel):
    id: int
    uid: str
    service: str
    license_key: Union[str, None]
    expires_at: Union[datetime, None]

class GrantUser(BaseModel):
    email: str
    service: str

class Comment(BaseModel):
    text: str

class UserComment(BaseModel):
    user: User
    comment: str
    created_at: datetime

__all__ = [
    "User",
    "SignIn",
    "AuthToken",
    "UserLog",
    "License",
    "GrantUser",
    "UserComment",
]
