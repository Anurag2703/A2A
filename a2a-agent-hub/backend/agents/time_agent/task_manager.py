from models.agent import AgentCard
import datetime

agent_card = AgentCard(
    id="time_agent",
    name="Time Informer",
    description="Tells the current date and time.",
    capabilities=["time"],
    icon_url=None
)

def run(task):
    now = datetime.datetime.now().isoformat()
    return {"success": True, "output": f"Current time: {now}"}
