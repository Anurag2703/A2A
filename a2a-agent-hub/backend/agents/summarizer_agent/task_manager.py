# ───────────────────────────────────────────────────────────────
# File: backend/agents/summarizer_agent/task_manager.py
# Purpose: Agent skill to summarize legal documents via Gemini
# ───────────────────────────────────────────────────────────────



import os
from google.generativeai import GenerativeModel, configure
from models.task import TaskRequest, TaskResponse
from models.agent import AgentCard
from core.config import settings
from core.aui import AUIResponse
import re
import json



# ──────────────── Gemini Configuration ────────────────
configure(api_key=settings.GEMINI_API_KEY)
model = GenerativeModel("gemini-1.5-flash")



# ──────────────── Agent Card ────────────────
agent_card = {
    "id": "summarizer_agent",
    "name": "Legal Document Summarizer",
    "description": "Summarizes legal documents into concise bullet points using Gemini AI.",
    "capabilities": ["summarization", "legal", "documents"],
    "author": "Your Name",
    "version": "1.0",
    "tags": ["summarization", "legal", "documents", "AI"],
    "input_example": {
        "prompt": "Summarize this NDA in bullet points.",
        "file_name": "nda.pdf",
        "summary_style": "concise"
    },
    "output_example": {
        "student_info": {},
        "courses": [],
        "performance": {},
        "status": ""
    }
}



# ──────────────── Main Task Processing Function ────────────────
import re
import json

async def run(prompt: str = None, file_path: str = None, summary_style: str = "concise") -> TaskResponse:
    try:
        from utils.file_parser import parse_file_to_text
        document_text = ""
        
        if file_path:
            document_text = parse_file_to_text(file_path)
            if not document_text.strip():
                try:
                    import pytesseract
                    from PIL import Image
                    from pdf2image import convert_from_path
                    pages = convert_from_path(file_path)
                    document_text = "\n".join(pytesseract.image_to_string(p) for p in pages)
                except Exception as ocr_err:
                    return TaskResponse(success=False, error=f"OCR failed: {ocr_err}")

        context = f"""
            You are an intelligent AI assistant that analyzes *any* type of document
            (e.g., marksheets, grade reports, legal documents, medical reports, question banks, etc.).
            Given the user's instruction and the document, produce a structured JSON summary
            that adapts to the document’s content.

            Guidelines:
            - Detect the type of document automatically.
            - Create relevant JSON keys that match the document type and content.
            - Use clear, human-readable keys and concise values.
            - If the document contains lists, tables, or bullet points, preserve them in arrays.
            - Do not include null fields unless absolutely necessary.
            - Output must be valid JSON only.

            Summary style: {summary_style}

            --- BEGIN USER PROMPT ---
            {prompt}
            --- END USER PROMPT ---

            --- BEGIN DOCUMENT TEXT ---
            {document_text[:8000]}
            --- END DOCUMENT TEXT ---
        """

        response = model.generate_content(context)
        raw_text = response.text.strip()

        # Strip code fences and parse JSON
        clean_text = re.sub(r"^```json\s*|\s*```$", "", raw_text, flags=re.DOTALL).strip()
        parsed_json = json.loads(clean_text)
        
        # Wrap into AUI protocol; we keep original parsed_json as content.data
        aui_resp = AUIResponse.success(
            agent_id="summarizer_agent",
            agent_name="Legal Document Summarizer",
            agent_version="1.0",
            content_data=parsed_json,
            content_type="structured",
            metadata={
                "document_type": None,
                "confidence": None,
                "processing_time_ms": None,
                "tokens_used": None,
                "model": "gemini-1.5-flash",
                "timestamp": None,
                "error": None
            },
            context={"source": os.path.basename(file_path) if file_path else None},
            raw_text=raw_text
        )

        return TaskResponse(success=True, output=aui_resp)
        # return TaskResponse(success=True, output=parsed_json)

    except json.JSONDecodeError:
        aui_err = AUIResponse.error(
            agent_id="summarizer_agent",
            agent_name="Legal Document Summarizer",
            error_message="Model did not return valid JSON.",
            metadata={"error": "json_decode_error"}
        )
        return TaskResponse(success=False, output=aui_err, error="Model did not return valid JSON.")
    
    except Exception as e:
        aui_err = AUIResponse.error(
            agent_id="summarizer_agent",
            agent_name="Legal Document Summarizer",
            error_message=str(e),
            metadata={"error": "exception"}
        )
        return TaskResponse(success=False, output=aui_err, error=str(e))
    # except json.JSONDecodeError:
    #     return TaskResponse(success=False, error="Model did not return valid JSON.")
    # except Exception as e:
    #     return TaskResponse(success=False, error=str(e))