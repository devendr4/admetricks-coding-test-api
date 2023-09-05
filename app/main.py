from fastapi import FastAPI

from app.dollar.router import router

app = FastAPI()

app.include_router(router)
