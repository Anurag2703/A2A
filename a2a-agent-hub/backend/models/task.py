# ───────────────────────────────────────────────────────────────
# File: backend/models/task.py
# Purpose: Pydantic models for incoming task request & output
# ───────────────────────────────────────────────────────────────

from pydantic import BaseModel
from typing import Optional, Any



# ──────────────── Task Request (from user/frontend) ────────────────
class TaskRequest(BaseModel):
    prompt: str                             # Prompt or question from the user
    agent_id: str                           # Which agent to use (e.g., "summarizer_agent")
    file_name: Optional[str] = None         # Original filename (for context)
    file_base64: Optional[str] = None       # File content (base64-encoded)
    file_mime_type: Optional[str] = None    # MIME type, e.g., "application/pdf"



# ──────────────── Task Response (from agent to user) ────────────────
class TaskResponse(BaseModel):
    success: bool
    output: Any = None     # can now be dict, list, string, etc.
    error: Optional[str] = None     # If success = False
