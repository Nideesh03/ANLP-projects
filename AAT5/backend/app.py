"""AAT-5 backend (Nideesh V, 1GA23AI028). Run: python app.py  ->  http://localhost:5105"""
import os
from flask import Flask, request, jsonify, send_from_directory
import core

FRONTEND = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")
app = Flask(__name__, static_folder=None)


@app.get("/")
def home():
    return send_from_directory(FRONTEND, "index.html")


@app.get("/<path:name>")
def assets(name):
    return send_from_directory(FRONTEND, name)


@app.post("/api/run")
def run():
    return jsonify(core.run(request.get_json(force=True)))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5105)))
