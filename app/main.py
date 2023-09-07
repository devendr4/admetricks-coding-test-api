from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.usd.router import router

app = FastAPI()
origins = ["http://localhost:5173", "http://localhost:4173", "*"]

app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"]
)
app.include_router(router)
