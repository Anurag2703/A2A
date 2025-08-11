# ───────────────────────────────────────────────────────────────
# File: backend/api/routes/agents.py
# Purpose: Returns metadata for all available agents
# ───────────────────────────────────────────────────────────────

from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from importlib import import_module
from pathlib import Path
from core.config import settings
from models.agent import AgentCard
from models.task import TaskRequest, TaskResponse
from agents import agent_registry
import tempfile
import shutil

router = APIRouter(prefix="/agents", tags=["Agents"])



# ──────────────── GET /agents/metadata ────────────────
@router.get("/metadata", response_model=list[AgentCard])
def list_available_agents():
    """
    Dynamically loads all AgentCard metadata from agent modules
    inside backend/agents/.
    """
    agents_path = Path(settings.AGENT_PATH).resolve()
    agent_cards = []

    for agent_folder in agents_path.iterdir():
        if agent_folder.is_dir() and (agent_folder / "task_manager.py").exists():
            module_path = f"agents.{agent_folder.name}.task_manager"
            try:
                mod = import_module(module_path)
                card = getattr(mod, "agent_card", None)
                if card:
                    agent_cards.append(card)
            except Exception as e:
                print(f"[ERROR] Could not load agent from {module_path}: {e}")

    return agent_cards



# ──────────────── POST /agents/run ────────────────
@router.post("/run", response_model=TaskResponse)
def run_agent_task(task: TaskRequest):
    """
    Executes a given task using the selected agent.
    """
    agent_path = f"agents.{task.agent_id}.task_manager"

    try:
        agent_module = import_module(agent_path)

        if not hasattr(agent_module, "run"):
            raise HTTPException(status_code=500, detail=f"Agent {task.agent_id} has no run() function.")

        result: TaskResponse = agent_module.run(task)
        return result

    except ModuleNotFoundError:
        raise HTTPException(status_code=400, detail=f"Unknown agent: {task.agent_id}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running agent: {str(e)}")



@router.post("/{agent_id}/run")
async def run_agent(
    agent_id: str,
    prompt: str = Form(...),
    file: UploadFile = File(None)
):
    agent = agent_registry.get(agent_id)
    if not agent:
        return {"error": "Agent not found"}

    file_path = None
    if file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(file.file, tmp)
            file_path = tmp.name

    result = await agent.run(prompt=prompt, file_path=file_path)
    return result