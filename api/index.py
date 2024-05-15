from fastapi import FastAPI
from api.routes import auth, user, admin


app = FastAPI(
    title="Vercel FastAPI",
    description="FastAPI hosted on Vercel",
    docs_url="/docs",
    redoc_url=None
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(admin.router)
