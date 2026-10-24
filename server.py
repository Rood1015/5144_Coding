from flask import Flask, jsonify, request
import logging
import os
import threading


os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/operations.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

store_lock = threading.Lock()

app = Flask(__name__)

# In-memory key-value storage
store = {}


@app.route("/<key>", methods=["POST", "PUT"])
def put_value(key):
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or "value" not in data:
        return jsonify({"error": "Request must contain a value"}), 400
    with store_lock:
        store[key] = data["value"]
    logging.info("POST key=%s status=200", key)
    return jsonify({"status": "ok"}), 200


@app.route("/<key>", methods=["GET"])
def get_value(key):
    with store_lock:
        if key not in store:
            logging.info("GET key=%s status=404", key)
            return jsonify({"error": "Key not found"}), 404
        value = store[key]
    logging.info("GET key=%s status=200", key)
    return jsonify({"value": value}), 200

@app.route("/<key>", methods=["DELETE"])
def delete_value(key):
    with store_lock:
        if key not in store:
            return jsonify({"error": "Key not found"}), 404
        del store[key]
    logging.info("DEL key=%s status=200", key)
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, threaded=True)
