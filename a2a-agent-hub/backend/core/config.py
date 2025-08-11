# ───────────────────────────────────────────────────────────────
# File: backend/core/config.py
# Purpose: Loads environment variables and configuration settings
# ───────────────────────────────────────────────────────────────


from pydantic_settings import BaseSettings
from pathlib import Path

# Points to backend/
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    POSTGRES_URI: str
    REDIS_URI: str = "redis://localhost:6379"
    AGENT_PATH: str = str(BASE_DIR / "agents")  # backend/agents absolute path

    class Config:
        env_file = ".env"

settings = Settings()
