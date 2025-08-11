# ───────────────────────────────────────────────────────────────
# File: backend/agents/summarizer_agent/task_manager.py
# Purpose: Agent skill to summarize legal documents via Gemini
# ───────────────────────────────────────────────────────────────



import os
from google.generativeai import GenerativeModel, configure
from models.task import TaskRequest, TaskResponse
from models.agent import AgentCard
from core.config import settings
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
            You are a legal expert AI assistant.
            Given the document below and the user's instruction, produce a structured JSON summary.

            JSON keys must be:
            - student_info: object with fields like name, roll_number, reg_number, admission_year, semester
            - courses: array of {{"name": string, "credits": number, "grade": string}}
            - performance: object with SGPA, CGPA, total_credits
            - status: "PASS" or "FAIL"

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

        return TaskResponse(success=True, output=parsed_json)

    except json.JSONDecodeError:
        return TaskResponse(success=False, error="Model did not return valid JSON.")
    except Exception as e:
        return TaskResponse(success=False, error=str(e))






# import os
# from google.generativeai import GenerativeModel, configure
# from models.task import TaskRequest, TaskResponse
# from models.agent import AgentCard
# from core.config import settings



# # ──────────────── Gemini Configuration ────────────────
# configure(api_key=settings.GEMINI_API_KEY)
# model = GenerativeModel("gemini-1.5-flash")



# # ──────────────── Agent Card ────────────────
# agent_card = AgentCard(
#     id="summarizer_agent",
#     name="Legal Document Summarizer",
#     description="Summarizes legal documents into concise bullet points using Gemini AI.",
#     capabilities=["summarization", "legal", "documents", "AI"],
#     icon_url=None
# )



# # ──────────────── Agent Metadata ────────────────
# agent_card = {
#     "id": "summarizer_agent",  # Unique ID for this agent
#     "name": "Legal Document Summarizer",
#     "description": "Summarizes legal documents into concise bullet points using Gemini AI.",
#     "capabilities": ["summarization", "legal", "documents"],
#     "author": "Your Name",
#     "version": "1.0",
#     "tags": ["summarization", "legal", "documents", "AI"],
#     "input_example": {
#         "prompt": "Summarize this NDA in bullet points.",
#         "file_name": "nda.pdf"
#     },
#     "output_example": {
#         "summary": [
#             "Parties agree to maintain confidentiality.",
#             "Information must not be disclosed without consent."
#         ]
#     }
# }



# # ──────────────── Main Task Processing Function ────────────────
# async def run(prompt: str = None, file_path: str = None) -> TaskResponse:
#     try:
#         context = f"""
#             You are a legal expert AI assistant. Given the document below and the user's instruction,
#             return a clean and concise summary in bullet points.

#             --- BEGIN USER PROMPT ---
#             {prompt}
#             --- END USER PROMPT ---
#         """

#         if file_path:
#             from utils.file_parser import parse_file_to_text
#             document_text = parse_file_to_text(file_path)
#             context += f"\n--- BEGIN DOCUMENT TEXT ---\n{document_text[:8000]}\n--- END DOCUMENT TEXT ---"

#         response = model.generate_content(context)
#         return TaskResponse(success=True, output=response.text)

#     except Exception as e:
#         return TaskResponse(success=False, error=str(e))