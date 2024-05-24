from typing import Union
from datetime import datetime
from pydantic import BaseModel

class UserProfileResponse(BaseModel):
    name: str

class UserLicenseResponse(BaseModel):
    service: str
    expires_at: Union[datetime, None]
