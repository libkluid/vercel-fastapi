from fastapi import FastAPI
from api.routes import debug, user

app = FastAPI()

app.include_router(debug.router)
app.include_router(user.router)
