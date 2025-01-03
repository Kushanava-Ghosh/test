from flask import Flask, request, jsonify

app = Flask(__name__)

# List to store all client IP addresses
client_ips = []

@app.route("/", methods=["GET", "POST"])
def home():
    # Get the client's IP address
    client_ip = request.remote_addr
    # Add the IP address to the list
    client_ips.append(client_ip)
    # Log the IP address (optional, for debugging)
    print(f"Client IP: {client_ip}")
    return "ok", 200

@app.route("/ips", methods=["GET"])
def list_ips():
    # Endpoint to list all collected IPs
    return jsonify(client_ips), 200

if __name__ == "__main__":
    app.run(debug=True)
