import socket
from uuid import getnode as get_mac
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/details")
def details():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    mac = ':'.join(("%012X" % get_mac())[i:i+2] for i in range(0, 12, 2))
    return jsonify(hostname=hostname, ip=ip, mac=mac)

@app.route("/")
def home():
    return "Hello Berkay Hocam"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
