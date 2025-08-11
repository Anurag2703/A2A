from models.agent import AgentCard

agent_card = AgentCard(
    id="math_agent",
    name="Math Solver",
    description="Performs basic math calculations.",
    capabilities=["calculation"],
    icon_url=None
)

def run(task):
    return {"success": True, "output": "Math agent not implemented yet."}
