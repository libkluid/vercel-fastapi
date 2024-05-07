from datetime import datetime
from pydantic import BaseModel

class User(BaseModel):
    id: int
    uid: str
    name: str
    email: str
    created_at: datetime
