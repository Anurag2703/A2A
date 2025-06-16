# ------------------------------------------------------------------------------
# 1. This file defines a very simple AI agent called TellTimeAgent.
# 2. It uses Google's ADK & Gemini Model to respond with the current time.
# ------------------------------------------------------------------------------


from datetime import datetime

# Gemini-based AI agent provided by Google's ADK 
from google.adk.agents.llm_agent import LlmAgent

# ADK services for session, memory, & file-like artifacts
from google.adk.sessions import InMemorySessionService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.artifacts import InMemoryArtifactService

# The "runner" connects the agent, session, memory & files into a complete system
from google.adk.runners import Runner

# Gemini-compatible types for formatting I/O messages
from google.genai import types

# Load environment variables (like API keys) from a '.env' file
from dotenv import load_dotenv
load_dotenv()   # Loads variables like GOOGLE_API_KEY into the system.
                # This allows me to keep sensitive data out of my code
                
                

# -------------------------------------------------
# TellTimeAgent: AI agent that tells the time
# -------------------------------------------------
class TellTimeAgent:
    # Supports only plain text I/O
    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]
    
    def __init__(self):
        """
            Initialize the TellTimeAgent:
                - Creates the LLM agent (powered by Gemini)
                - Sets up session handling, memory, and a runner to execute tasks
        """
        
        self._agent = self._build_agent()   # Set up the Gemini agent
        self._user_id = "time_agent_user"   # Use a fixed user ID for simplicity
        
        # The Runner is what actually manages the agent and its environment
        self._runner = Runner(
            app_name = self._agent.name,
            agent = self._agent,
            artifact_service = InMemoryArtifactService(),     # For files (not used here)
            session_service = InMemorySessionService(),       # Keeps track of conversations
            memory_service = InMemoryMemoryService(),        # Optional: remembers past messages
        )
        
    
    def _build_agent(self) -> LlmAgent:
        """
            Creates and returns a Gemini agent with basic settings.

            Returns:
                LlmAgent: An agent object from Google's ADK
        """
        return LlmAgent(
            model="gemini-1.5-flash-latest",        # Gemini model version
            name="tell_time_agent",                 # Name of the agent
            description="Tells the current time",   # Description for metadata
            instruction="Reply with the current time in the format YYYY-MM-DD HH:MM:SS." # System Prompt
        )
        
    
    def invoke(self, query: str, session_id: str) -> str:
        """
            Handle a user query and return a response string.

            Args:
                query (str): What the user said (e.g., "what time is it?")
                session_id (str): Helps group messages into a session

            Returns:
                str: Agent's reply (usually the current time)
        """
        
        # Try to reuse an existing session
        session = self._runner.session_service.get_session(
            app_name=self._agent.name,
            user_id=self._user_id,
            session_id=session_id
        )
        
        # or create a session if needed
        if session is None:
            session = self._runner.session_service.create_session(
                app_name = self._agent.name,
                user_id = self._user_id,
                session_id = session_id,
                state = {}      # Optional dictionary to hold session state
            )
            
        # Format the user message in a way the Gemini model expects
        content = types.Content(
            role = "user",
            parts = [types.Part.from_text(text=query)]
        )
        
        # Run the agent using the Runner and collect the response events
        events = list(self._runner.run(
            user_id = self._user_id,
            session_id = session.id,
            new_message = content
        ))
        
        # Fallback: return empty string if something went wrong
        if not events or not events [-1].content or not events [-1].content.parts:
            return ""

        # Extract and join all text responses into one string
        return "\n".join([p.text for p in events [-1].content.parts if p.text])
    
    
    
    
    
    # CURRENTLY THIS AGENT DOES NOT SUPPORT STREAM
    async def stream(self, query: str, session_id: str):
        """
            Stimulates a "streaming" agent that returns a single reply.
            This just demonstrates that STREAMING is possible

            Yields:
                dict: Response payload that says the task is complete and gives the time
        """
        
        yield {
            "is_task_complete": True,
            "content": f"The current time is: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        }