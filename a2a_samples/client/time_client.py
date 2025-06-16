import requests     # Helps to send HTTP GET & POST requests
import uuid         # Generates unique task IDs as A2A tasks need to have Unique-IDs


# -------------------------------------------------
# Step-1: Discover the agent
# -------------------------------------------------

base_url = "http://localhost:5000"


# Using HTTP GET to fetch agent's card from the Well-Known-Discovery-Endpoint
res = requests.get(f"{base_url}/.well-known/agent.json")

# If request fails, then raise an error
if res.status_code != 200:
    raise Exception('Failed to discover agent!')

# Parses the JSON into a Python Dictionary
agent_info = res.json()

# Displays basic info about discovered agent.
print(f"Connected to: {agent_info['name']} ⬢ {agent_info['description']}")



# -------------------------------------------------
# Step-2: Prepare a Task
# -------------------------------------------------

task_id = str(uuid.uuid4())     # Generates unique ID for this task

# Construct an A2A task payload as a Python Dictionary
task_payload = {
    "id" : task_id,
    "message" : {
        "role" : "user",    # Message is coming from user
        "parts" : [
            {"text" : "What time is it?"}   # This is the question the user is asking
        ]
    }
}



# -------------------------------------------------
# Step-3: Send the Task to the Agent
# -------------------------------------------------

# Send HTTP POST request to the /tasks/send endpoint of the agent
response = requests.post(f"{base_url}/tasks/send", json=task_payload)

# If server doesn't returns the "200 OK" status, raise an error.
if response.status_code != 200:
    raise Exception(f"Task failed: {response.text}")

# Parse the agent's JSON response to the Python Dict.
response_data = response.json()



# -------------------------------------------------
# Step-4: Display the Agent's response
# -------------------------------------------------

# Extracts the list of messages returned in the response
messages = response_data.get("messages", [])

# If there are any message, extract & print the last one (agent's response)
if messages:
    final_reply = messages[-1]["parts"][0]["text"]
    print("🤖 Agent: ", final_reply)
else:
    print("No response!")