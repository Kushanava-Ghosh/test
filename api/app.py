from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app)

# List to hold connected clients
connected_clients = []

# When a client connects, we add them to the list
@socketio.on('connect')
def handle_connect():
    client_address = request.remote_addr  # or use socket.id for unique identification
    if client_address not in connected_clients:
        connected_clients.append(client_address)
    print(f"Client {client_address} connected. Total clients: {len(connected_clients)}")
    
    # Emit the list of connected clients to all clients
    emit('clients_list', connected_clients, broadcast=True)

# When a client disconnects, remove them from the list
@socketio.on('disconnect')
def handle_disconnect():
    client_address = request.remote_addr
    if client_address in connected_clients:
        connected_clients.remove(client_address)
    print(f"Client {client_address} disconnected. Total clients: {len(connected_clients)}")
    
    # Emit the updated list of connected clients
    emit('clients_list', connected_clients, broadcast=True)

# Route for testing the connection (optional)
@app.route('/')
def index():
    return 'Flask WebSocket Server - Connected Clients will be listed in the console.'

# Start the Flask app
if __name__ == '__main__':
    socketio.run(app, debug=True)
