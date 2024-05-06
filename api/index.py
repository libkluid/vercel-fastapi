from fastapi import FastAPI
from api.routes import debug

app = FastAPI()

app.include_router(debug.router)
