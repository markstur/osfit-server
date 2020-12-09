
from flask import jsonify
from server import app
from server.routes import prometheus

@app.route("/health")
@prometheus.track_requests
def health():
    """health route"""
    state = {"status": "UP"}
    return jsonify(state)
