from flask import Flask, request

app = Flask(__name__)

# Data storage
rooms = {}  # Stores room data in the form {room_id: {"clients": [], "messages": []}}

@app.route("/")
def list_rooms():
    """List all active rooms and their clients."""
    if not rooms:
        return "No active rooms."
    
    result = "Active Rooms:\n"
    for room_id, data in rooms.items():
        clients = ", ".join(data["clients"]) if data["clients"] else "No clients"
        result += f"Room ID: {room_id}, Clients: {clients}\n"
    return result

# @app.route("/register", methods=["GET"])
# def register():
#     return """
#     Choose an option:
#     1. Create Room: Visit /create-room
#     2. Join Room: Visit /join-room?room_id=<room-id>
#     """

@app.route("/create-room", methods=["GET"])
def create_room():
    import uuid
    # Generate a unique room ID
    room_id = str(uuid.uuid4())[:8]  # Shortened UUID for simplicity
    rooms[room_id] = {"clients": []}
    # return f"Room created successfully! Room ID: {room_id}\nYou can access the room at /{room_id}"
    return f"{room_id}"

@app.route("/join-room", methods=["GET"])
def join_room():
    room_id = request.args.get("room_id")
    client_ip = request.remote_addr

    if not room_id or room_id not in rooms:
        return "Room ID is invalid or does not exist."

    # Check if the room already has two clients
    if len(rooms[room_id]["clients"]) >= 2:
        return "Room is full. You cannot join."
        
    # Add the client to the room if not already present
    if client_ip not in rooms[room_id]["clients"]:
        rooms[room_id]["clients"].append(client_ip)
        
    rooms[room_id][client_ip] = "No messages"

    if len(rooms[room_id]["clients"]) == 2:
        for key, value in rooms[room_id].items():
            if key != "clients":
                rooms[room_id][key] = "START"
    
    # return f"Joined room {room_id}. You can send and receive messages using /{room_id}."
    return f"Joined room {room_id}"

@app.route("/<room_id>", methods=["GET", "POST"])
def room_communication(room_id):
    client_ip = request.remote_addr
    
    if room_id not in rooms:
        return "Room does not exist."

    if request.method == "GET":
        # Fetch all messages in the room
        messages = ""
        for key, value in rooms[room_id].items():
            if key != "clients" and key != client_ip:
                messages = rooms[room_id][key]
                rooms[room_id][key] = "No messages"
        return messages

    elif request.method == "POST":
        # Add a new message to the room
        message = request.form.get("message")

        if client_ip not in rooms[room_id]["clients"]:
            return "You are not a participant in this room."

        if not message:
            return "Message cannot be empty."

        rooms[room_id][client_ip] = message
        return "Message sent successfully."

if __name__ == "__main__":
    app.run(debug=True)
