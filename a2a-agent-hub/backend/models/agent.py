# ───────────────────────────────────────────────────────────────
# File: backend/models/agent.py
# Purpose: Pydantic schema for agent metadata (AgentCard)
# ───────────────────────────────────────────────────────────────

from pydantic import BaseModel
from typing import List, Optional



# ──────────────── AgentCard: Describes an agent's identity & purpose ────────────────
class AgentCard(BaseModel):
    id: str                             # Unique agent identifier
    name: str                           # Friendly display name
    description: str                    # What the agent does
    capabilities: List[str]             # Skills (e.g., summarization, math, OCR)
    icon_url: Optional[str] = None      # Optional frontend icon for the agent
