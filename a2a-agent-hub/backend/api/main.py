# ───────────────────────────────────────────────────────────────
# File: backend/api/main.py
# Purpose: FastAPI entrypoint for A2A Agent Hub
# ───────────────────────────────────────────────────────────────



# ──────────────── 1. Imports ────────────────
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from core.config import settings
from core.config import settings
from .routes import agents  # dynamic agents routes



# ──────────────── Create FastAPI App ────────────────
app = FastAPI(
    title="A2A Agent Hub",
    description="Multi-Agent Hub with dynamic agent loading",
    version="1.0.0"
)



# ──────────────── Enable CORS ────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, replace "*" with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ──────────────── Register Routes ────────────────
app.include_router(agents.router)



# ──────────────── Root Endpoint ────────────────
@app.get("/")
def root():
    return {"message": "Welcome to A2A Agent Hub API", "agents_path": settings.AGENT_PATH}