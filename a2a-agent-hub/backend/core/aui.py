import json
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from jsonschema import validate, ValidationError
import os

# Load schema from file next to this module
_SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "aui_schema.json")
with open(_SCHEMA_PATH, "r", encoding="utf-8") as f:
    AUI_SCHEMA = json.load(f)


class AUIResponse:
    """
        Helper to build/validate AUI protocol responses.
        This is a simple wrapper — it does not change the agent's internal output,
        only wraps it to the AUI contract.
    """

    @staticmethod
    def _now_iso() -> str:
        return datetime.utcnow().isoformat() + "Z"

    @staticmethod
    def _default_metadata(document_type: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
        return {
            "document_type": document_type,
            "confidence": None,
            "processing_time_ms": None,
            "tokens_used": None,
            "model": model,
            "timestamp": AUIResponse._now_iso(),
            "error": None
        }

    @staticmethod
    def success(
        agent_id: str,
        agent_name: str,
        content_data: Any,
        content_type: str = "structured",
        agent_version: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        actions: Optional[list] = None,
        raw_text: Optional[str] = None
    ) -> Dict[str, Any]:
        body = {
            "version": "1.0",
            "status": "success",
            "agent": {"id": agent_id, "name": agent_name, "version": agent_version or "1.0"},
            "metadata": metadata or AUIResponse._default_metadata(),
            "context": context or {},
            "content": {
                "type": content_type,
                "title": None,
                "summary_text": None,
                "data": content_data
            },
            "actions": actions or [],
            "raw_text": raw_text
        }
        # validate before returning; if invalid, return best-effort but include validation error in metadata.error
        try:
            validate(instance=body, schema=AUI_SCHEMA)
        except ValidationError as ve:
            # attach validation problem but still return a structured wrapper
            body["metadata"]["error"] = f"AUI validation failed: {ve.message}"
        return body

    @staticmethod
    def error(
        agent_id: str,
        agent_name: str,
        error_message: str,
        metadata: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        body = {
            "version": "1.0",
            "status": "error",
            "agent": {"id": agent_id, "name": agent_name, "version": None},
            "metadata": (metadata or AUIResponse._default_metadata()),
            "context": context or {},
            "content": {
                "type": "error",
                "title": "Error",
                "summary_text": error_message,
                "data": {}
            },
            "actions": [],
            "raw_text": None
        }
        body["metadata"]["error"] = error_message
        return body

    @staticmethod
    def partial(
        agent_id: str,
        agent_name: str,
        content_data: Any,
        content_type: str = "stream",
        metadata: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        body = {
            "version": "1.0",
            "status": "partial",
            "agent": {"id": agent_id, "name": agent_name, "version": None},
            "metadata": metadata or AUIResponse._default_metadata(),
            "context": context or {},
            "content": {
                "type": content_type,
                "title": None,
                "summary_text": None,
                "data": content_data
            },
            "actions": [],
            "raw_text": None
        }
        return body