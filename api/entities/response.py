from pydantic import BaseModel

class UserInfoResponse(BaseModel):
    uid: str
    email: str
    name: str
    created_at: str
    updated_at: str
