1. Create a virtual environment:
    python -m venv .venv

2. Start a virtual environment:
    .venv\Scripts\Activate.ps1 

3. Shut down virtual environment:
    deactivate

4. Install ADK (after virtual environment is active):
    pip install google-adk

5. Verify ADK:
    pip show google-adk 




(IN SEPARATE TERMINALS)

1.  To start the agent:
        python -m agents.google_adk

2.  To start the client:
        python -m app.cmd.cmd --agent http://localhost:10002