# ───────────────────────────────────────────────────────────────
# File: backend/api/deps/dependencies.py
# Purpose: Dependency injection for agent loading and memory
# ───────────────────────────────────────────────────────────────

from importlib import import_module
from typing import Dict
from core.config import settings



# ──────────────── Memory Store (Mock) ────────────────
# Later: Replace this with Redis or Postgres implementation
_memory_store: Dict[str, list] = {}

def get_memory_store() -> Dict[str, list]:
    """
    Provides a per-session memory dictionary (mock).
    Replace with persistent Redis/Postgres layer later.
    """
    return _memory_store




# ──────────────── Agent Loader ────────────────
def get_agent_by_name(agent_name: str):
    """
    Dynamically loads agent implementation from agents/<agent_name>/task_manager.py
    Returns the `Agent` class instance with a `.run()` method.
    """
    try:
        module_path = f"agents.{agent_name}.task_manager"
        module = import_module(module_path)
        return getattr(module, "agent_instance", None)
    except Exception as e:
        print(f"[ERROR] Failed to load agent '{agent_name}': {e}")
        return None
