from flask import Flask, request, jsonify    # Import the Flask & utility functions from the flask package.
from datetime import datetime    # Use this to get the current date & time

app = Flask(__name__)    # Initializing so that endpoints defined on it


# -------------------------------------------------
# Endpoint: Agent Card (Discovery Phase)
# -------------------------------------------------

# Defining an HTTP GET route for well-known agent discovery path.
@app.route("/.well-known/agent.json", methods=["GET"])
def agent_card():
    # returns metadata about the agent in JSON format.
    return jsonify({
        'name' : 'TellTimeAgent',
        'description' : 'Tells the current time when asked',   # No LLM is invoked. Directly uses the datetime library to tell the time
        'url' : 'http://localhost:5000',    # Where the agent is hosted
        'version' : '1.0',
        'capabilities' : {
            'streaming' : 'False',          # The agent doesn't support real-time updates to the client
            'PushNotifications' : 'False'   # The agent doesn't support Push-Notification
        }
    })
    
    

# -------------------------------------------------
# Endpoint: Task Handling (tasks/send)
# -------------------------------------------------

# This is the main endpoint that A2A clients use a send task to the agent
@app.route("/tasks/send", methods=["POST"])    # HTTP GET route at task/send
def handle_task():
    try:
        task = request.get_json()   # Parsing the JSON payload into a Python dictionary
        
        task_id = task.get('id')    # Extract the task ID from the payload
        
        user_message = task['message']['parts'][0]['text']  # Extract user message from the 1st message part 
    
    except(KeyError, IndexError, TypeError):
        return jsonify({
            "error" : "Invalid Task Format!"
        }), 400
        
    # -------------------------------------------------
    # Generate a response to the user message
    # -------------------------------------------------

    # Get current system time as a formatted string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    reply_text = f'The current time is: {current_time}'

    # Returns a proper formatted A2A task response (includes the OG message & new message from the agent)
    return jsonify({
        "id" : task_id,
        "status" : {"state" : "completed"},
        "messages" : [
            task["message"], # Include the original user message for context
            {
                "role" : "agent",
                "parts" : [{"text" : reply_text}]
            }
        ]
    })





# -------------------------------------------------
# Running the Flask server
# -------------------------------------------------
if __name__ == "__main__":
    app.run(port=5000)