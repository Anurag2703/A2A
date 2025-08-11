# backend/agents/__init__.py

from pathlib import Path
from importlib import import_module

agent_registry = {}



# ──────────────── Discover all agent modules ────────────────
agents_path = Path(__file__).parent

for agent_dir in agents_path.iterdir():
    if agent_dir.is_dir() and (agent_dir / "task_manager.py").exists():
        module_path = f"agents.{agent_dir.name}.task_manager"  # removed 'backend.'
        try:
            mod = import_module(module_path)
            if hasattr(mod, "agent_card") and hasattr(mod, "run"):
                agent_registry[agent_dir.name] = mod
        except Exception as e:
            print(f"[ERROR] Failed to import {module_path}: {e}")