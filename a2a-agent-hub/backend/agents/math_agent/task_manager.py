# backend/agents/math_agent/task_manager.py
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
    "id": "math_agent",
    "name": "Math Problem Solver",
    "description": "Solves mathematical problems and returns steps + final answer.",
    "capabilities": ["math", "calculation"],
    "version": "1.0",
}

async def run(prompt: str = None, **kwargs) -> TaskResponse:
    try:
        # Build prompt: ask Gemini to return JSON only
        context = f"""
You are a precise math assistant. Interpret the user's prompt and
return a JSON object with two fields:
- steps: an array of strings describing the step-by-step solution (concise)
- final_answer: a string with the final numeric or symbolic answer

Only output valid JSON and nothing else.

User prompt:
{prompt}
"""
        response = model.generate_content(context)
        raw_text = response.text.strip()
        clean_text = re.sub(r"^```json\s*|\s*```$", "", raw_text, flags=re.DOTALL).strip()
        parsed = json.loads(clean_text)

        aui = AUIResponse.success(
            agent_id="math_agent",
            agent_name="Math Problem Solver",
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
            agent_id="math_agent",
            agent_name="Math Problem Solver",
            error_message="Model did not return valid JSON.",
            metadata={"error": "json_decode_error"}
        )
        return TaskResponse(success=False, output=aui_err, error="Invalid JSON from model.")
    except Exception as e:
        aui_err = AUIResponse.error(
            agent_id="math_agent",
            agent_name="Math Problem Solver",
            error_message=str(e),
            metadata={"error": "exception"}
        )
        return TaskResponse(success=False, output=aui_err, error=str(e))
