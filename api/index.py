from fastapi import FastAPI
from api.routes import debug

app = FastAPI(
    title="FastAPI Demo",
    description="This is a simple FastAPI demo.",
    version="0.1",
    docs_url="/docs",
    redoc_url=None,
)

app.include_router(debug.router)
