
import os
import requests

from flask import Flask, request, jsonify
from consistent_hash import ConsistentHash

app = Flask(__name__)

@app.route("/", methods=["GET"])
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "kv-router",
        "stores": len(KV_STORES)
    }), 200

# Addresses of the KV Store instances
KV_STORES = os.environ.get(
    "KV_STORES",
    "http://kv1:8080,http://kv2:8080,http://kv3:8080"
).split(",")

# Create the consistent hashing ring
hash_ring = ConsistentHash(KV_STORES, replicas=500)


@app.route("/<key>", methods=["GET", "POST", "PUT", "DELETE"])
def handle_request(key):

    # 1. Determine which KV Store owns this key
    target_server = hash_ring.get_node(key)

    if target_server is None:
        return jsonify({"error": "No KV Store available"}), 503

    # 2. Forward the client's request
    try:

        if request.method == "POST":
            response = requests.post(
                f"{target_server}/{key}",
                json=request.get_json(),
                timeout=5
            )
        elif request.method == "PUT":
            response = requests.put(
                f"{target_server}/{key}",
                json=request.get_json(),
                timeout=5
            )
        elif request.method == "GET":
            response = requests.get(
                f"{target_server}/{key}",
                timeout=5
            )
        elif request.method == "DELETE":
            response = requests.delete(
                f"{target_server}/{key}",
                timeout=5
            )
        # 3. Return the original KV Store response
        return (
            response.content,
            response.status_code,
            {"Content-Type": response.headers.get(
                "Content-Type", "application/json"
            )}
        )
    except requests.RequestException as e:

        return jsonify({
            "error": "KV Store unavailable",
            "details": str(e)
        }), 503

if __name__ == "__main__":
    PORT = int(os.environ.get("ROUTER_PORT", 5555))
    app.run(host="0.0.0.0", port=PORT, threaded=True)
