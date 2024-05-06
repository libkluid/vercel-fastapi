from pydantic import BaseModel, Field

class DebugTimeResponse(BaseModel):
    time: str = Field(
        default=...,
        title="Current time",
        description="Current time in ISO format"
    )
