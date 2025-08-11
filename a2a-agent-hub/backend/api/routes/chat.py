# ───────────────────────────────────────────────────────────────
# File: backend/api/routes/chat.py
# Purpose: Route for chatbot interaction – prompt + file upload
#              Interacts with the appropriate agent and returns result
# ───────────────────────────────────────────────────────────────

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import base64
import uuid

from core.config import settings
from utils.file_parser import parse_uploaded_file
from api.dependencies.dependencies import get_memory_store, get_agent_by_name

router = APIRouter()

# ──────────────── POST /chat/ ────────────────
@router.post("/")
async def chat_with_agent(
    prompt: str = Form(...),
    agent_name: str = Form(...),
    file: Optional[UploadFile] = File(None),
    session_id: Optional[str] = Form(None),
    memory_store=Depends(get_memory_store)
):
    """
    Accepts a user prompt and an optional file (PDF/image),
    processes with specified agent and returns response.
    """

    # ───────────── Generate or Retrieve Session ID ─────────────
    session_id = session_id or str(uuid.uuid4())

    # ───────────── Base64 Encode File (if present) ─────────────
    encoded_file = None
    if file:
        try:
            encoded_file = await parse_uploaded_file(file)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")

    # ───────────── Retrieve the Requested Agent ─────────────
    agent = get_agent_by_name(agent_name)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    # ───────────── Retrieve Memory (Context) ─────────────
    memory = memory_store.get(session_id, [])

    # ───────────── Agent Request & Response ─────────────
    response = agent.run(
        prompt=prompt,
        memory=memory,
        encoded_file=encoded_file
    )

    # ───────────── Update Memory ─────────────
    memory.append({"prompt": prompt, "response": response})
    memory_store[session_id] = memory

    # ───────────── Return JSON ─────────────
    return JSONResponse({
        "response": response,
        "session_id": session_id,
        "agent": agent_name
    })
