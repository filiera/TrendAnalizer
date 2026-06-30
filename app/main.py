from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes_hashtags import router as hashtags_router

app = FastAPI(title="Trend Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hashtags_router)