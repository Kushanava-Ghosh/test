from flask import Flask, request, jsonify

app = Flask(__name__)

# Shared dictionary to store messages for clients
messages = {
    "client1": None,  # Message for client1
    "client2": None   # Message for client2
}

@app.route("/send", methods=["POST"])
def send_message():
    # Get the sender and message from the form data
    sender = request.form.get("sender")
    message = request.form.get("message")

    if sender == "client1":
        # Store the message for client2
        messages["client2"] = message
    elif sender == "client2":
        # Store the message for client1
        messages["client1"] = message
    else:
        return "Invalid sender", 400

    return "Message sent", 200

@app.route("/receive", methods=["GET"])
def receive_message():
    # Get the client identifier from query parameters
    client = request.args.get("client")

    if client not in messages:
        return "Invalid client", 400

    # Get the message for the client
    message = messages[client]
    # Clear the message after delivering
    messages[client] = None

    if message is None:
        return "No messages", 200
    return f"Message: {message}", 200

if __name__ == "__main__":
    app.run(debug=True)
