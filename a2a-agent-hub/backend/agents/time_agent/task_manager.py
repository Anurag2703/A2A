# backend/agents/time_agent/task_manager.py
import os
from google.generativeai import GenerativeModel, configure
from models.task import TaskResponse
from core.config import settings
from core.aui import AUIResponse
import re
import json

configure(api_key=settings.GEMINI_API_KEY)
model = GenerativeModel("gemini-1.5-flash")

agent_card = {
    "id": "time_agent",
    "name": "Date & Time Assistant",
    "description": "Answers date/time queries; returns calculation steps and ISO result where applicable.",
    "capabilities": ["time", "date", "duration"],
    "version": "1.0",
}

async def run(prompt: str = None, **kwargs) -> TaskResponse:
    try:
        context = f"""
You are a date/time assistant. Interpret the user's prompt and return a JSON object:
- query: original prompt
- calculation: short explanation of how you computed the result
- result: the final result (use ISO date format for dates when applicable)

Output valid JSON only.

Prompt:
{prompt}
"""
        response = model.generate_content(context)
        raw_text = response.text.strip()
        clean_text = re.sub(r"^```json\s*|\s*```$", "", raw_text, flags=re.DOTALL).strip()
        parsed = json.loads(clean_text)

        aui = AUIResponse.success(
            agent_id="time_agent",
            agent_name="Date & Time Assistant",
            agent_version="1.0",
            content_data=parsed,
            content_type="structured",
            metadata={"model": "gemini-1.5-flash"},
            context={"query": prompt},
            raw_text=raw_text
        )
        return TaskResponse(success=True, output=aui)

    except json.JSONDecodeError:
        aui_err = AUIResponse.error(
            agent_id="time_agent",
            agent_name="Date & Time Assistant",
            error_message="Model did not return valid JSON.",
            metadata={"error": "json_decode_error"}
        )
        return TaskResponse(success=False, output=aui_err, error="Invalid JSON from model.")
    except Exception as e:
        aui_err = AUIResponse.error(
            agent_id="time_agent",
            agent_name="Date & Time Assistant",
            error_message=str(e),
            metadata={"error": "exception"}
        )
        return TaskResponse(success=False, output=aui_err, error=str(e))
