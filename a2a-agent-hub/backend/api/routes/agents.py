# backend/api/routes/agents.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import importlib
import os
import shutil
import tempfile
import typing as t
import re
from pathlib import Path

router = APIRouter()

# ──────────────────────────────
# Helper: detect agent based on prompt content
# ──────────────────────────────
def detect_agent_from_prompt(prompt: str) -> str:
    if not prompt:
        return ""
    p = prompt.lower().strip()

    # Math detection
    math_keywords = [
        r"\bsolve\b", r"\bcalculate\b", r"\bcompute\b", r"\bintegral\b",
        r"\bderivative\b", r"[\d]+\s*[\+\-\*\/\^=]", r"\bwhat is\b", r"\bsimplify\b"
    ]
    for pattern in math_keywords:
        if re.search(pattern, p):
            return "math_agent"

    # Time/date detection
    time_keywords = [
        r"\btoday\b", r"\btomorrow\b", r"\bday of\b", r"\bdays? from\b",
        r"\bwhat day\b", r"\bdate\b", r"\btimezone\b", r"\btime\b", r"\bwhen\b"
    ]
    for pattern in time_keywords:
        if re.search(pattern, p):
            return "time_agent"

    return ""


# ──────────────────────────────
# Internal: dynamically run an agent's task_manager
# ──────────────────────────────
async def call_agent_run_module(agent_id: str, prompt: str = None, file_path: str = None, **kwargs):
    """
    Dynamically import agent's task_manager and call its run() function.
    Each agent module must have an async run(...) -> TaskResponse or dict.
    """
    module_name = f"agents.{agent_id}.task_manager"
    try:
        mod = importlib.import_module(module_name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found: {e}")

    if not hasattr(mod, "run"):
        raise HTTPException(status_code=500, detail=f"Agent '{agent_id}' has no run() function.")

    run_fn = getattr(mod, "run")
    if file_path:
        resp = await run_fn(prompt=prompt, file_path=file_path, **kwargs)
    else:
        resp = await run_fn(prompt=prompt, **kwargs)

    # Normalize TaskResponse
    try:
        output = getattr(resp, "output", None)
        success = getattr(resp, "success", None)
        error = getattr(resp, "error", None)
        if output is not None:
            return {"success": success, "output": output, "error": error}
        else:
            return resp
    except Exception:
        return resp


# ──────────────────────────────
# Main run route
# ──────────────────────────────
@router.post("/agents/{agent_id}/run")
async def agent_run_route(
    agent_id: str,
    prompt: str = Form(None),
    file: UploadFile = File(None),
):
    """
    Unified run endpoint:
    - If file is uploaded → run the given agent_id (current flow preserved)
    - If no file → auto-detect math_agent or time_agent from prompt, else fallback to agent_id
    """
    if not prompt and not file:
        raise HTTPException(status_code=400, detail="Either prompt or file must be provided.")

    selected_agent = agent_id

    if file is None:  # Try detecting agent from prompt
        detected = detect_agent_from_prompt(prompt or "")
        if detected:
            selected_agent = detected

    temp_file_path = None
    try:
        if file is not None:
            suffix = Path(file.filename).suffix or ""
            fd, temp_file_path = tempfile.mkstemp(suffix=suffix)
            os.close(fd)
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

        result = await call_agent_run_module(selected_agent, prompt=prompt, file_path=temp_file_path)

        if isinstance(result, dict) and "output" in result:
            return JSONResponse(content=result["output"])  # Pass directly to AUI UniversalRenderer
        else:
            return JSONResponse(content=result)

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception:
                pass





# # ───────────────────────────────────────────────────────────────
# # File: backend/api/routes/agents.py
# # Purpose: Returns metadata for all available agents
# # ───────────────────────────────────────────────────────────────

# from fastapi import APIRouter, HTTPException, File, UploadFile, Form
# from importlib import import_module
# from pathlib import Path
# from core.config import settings
# from models.agent import AgentCard
# from models.task import TaskRequest, TaskResponse
# from agents import agent_registry
# import tempfile
# import shutil

# router = APIRouter(prefix="/agents", tags=["Agents"])



# # ──────────────── GET /agents/metadata ────────────────
# @router.get("/metadata", response_model=list[AgentCard])
# def list_available_agents():
#     """
#     Dynamically loads all AgentCard metadata from agent modules
#     inside backend/agents/.
#     """
#     agents_path = Path(settings.AGENT_PATH).resolve()
#     agent_cards = []

#     for agent_folder in agents_path.iterdir():
#         if agent_folder.is_dir() and (agent_folder / "task_manager.py").exists():
#             module_path = f"agents.{agent_folder.name}.task_manager"
#             try:
#                 mod = import_module(module_path)
#                 card = getattr(mod, "agent_card", None)
#                 if card:
#                     agent_cards.append(card)
#             except Exception as e:
#                 print(f"[ERROR] Could not load agent from {module_path}: {e}")

#     return agent_cards



# # ──────────────── POST /agents/run ────────────────
# @router.post("/run", response_model=TaskResponse)
# def run_agent_task(task: TaskRequest):
#     """
#     Executes a given task using the selected agent.
#     """
#     agent_path = f"agents.{task.agent_id}.task_manager"

#     try:
#         agent_module = import_module(agent_path)

#         if not hasattr(agent_module, "run"):
#             raise HTTPException(status_code=500, detail=f"Agent {task.agent_id} has no run() function.")

#         result: TaskResponse = agent_module.run(task)
#         return result

#     except ModuleNotFoundError:
#         raise HTTPException(status_code=400, detail=f"Unknown agent: {task.agent_id}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error running agent: {str(e)}")



# @router.post("/{agent_id}/run")
# async def run_agent(
#     agent_id: str,
#     prompt: str = Form(...),
#     file: UploadFile = File(None)
# ):
#     agent = agent_registry.get(agent_id)
#     if not agent:
#         return {"error": "Agent not found"}

#     file_path = None
#     if file:
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#             shutil.copyfileobj(file.file, tmp)
#             file_path = tmp.name

#     result = await agent.run(prompt=prompt, file_path=file_path)
#     return result