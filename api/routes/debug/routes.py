from fastapi import APIRouter
from api.service import time
from .response import DebugTimeResponse

router = APIRouter(prefix="/debug", tags=["debug"])

@router.get(
    path="/time",
    summary="Get the current time",
    description="Returns the current server time in ISO format",
    responses={
        200: {
            "model": DebugTimeResponse,
            "description": "Returns the current server time",
            "content": {
                "application/json": {
                    "example": {
                        "time": time.format(time.utc())
                    }
                }
            }
        }
    }
)
def server_time():
    return DebugTimeResponse.model_validate({
        "time": time.format(time.utc())
    })
