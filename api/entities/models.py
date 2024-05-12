from pydantic import BaseModel

class SignIn(BaseModel):
    email: str
    password: str

class AuthToken(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str

__all__ = [
    "SignIn",
]
