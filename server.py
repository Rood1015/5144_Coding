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

storage_lock = threading.Lock()

app = Flask(__name__)

storage = {}

@app.route("/<key>", methods=["POST", "PUT"])
def put_value(key):
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or "value" not in data:
        logging.info("%s key=%s status=400", request.method, key)
        return jsonify({"error": "Request must contain a value"}), 400
    with storage_lock:
        storage[key] = data["value"]
    logging.info("%s key=%s status=200", request.method, key)
    return jsonify({"status": "ok"}), 200


@app.route("/<key>", methods=["GET"])
def get_value(key):
    with storage_lock:
        if key not in storage:
            logging.info("GET key=%s status=404", key)
            return jsonify({"error": "Key not found"}), 404
        value = storage[key]
    logging.info("GET key=%s status=200", key)
    return jsonify({"value": value}), 200

@app.route("/<key>", methods=["DELETE"])
def delete_value(key):
    with storage_lock:
        if key not in storage:
            logging.info("DELETE key=%s status=404", key)
            return jsonify({"error": "Key not found"}), 404
        del storage[key]
    logging.info("DELETE key=%s status=200", key)
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, threaded=True)
