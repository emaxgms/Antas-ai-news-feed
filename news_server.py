#!/usr/bin/env python3
import json, os, threading
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
ITEMS_FILE = BASE_DIR / "items.json"
app = Flask(__name__, static_folder=".")

lock = threading.Lock()

@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/api/items")
def get_items():
    with lock:
        if not ITEMS_FILE.exists():
            return jsonify([])
        data = json.loads(ITEMS_FILE.read_text(encoding="utf-8"))
    # Ordina per data di pubblicazione (o added_at come fallback)
    data.sort(key=lambda x: x.get("published_at") or x.get("added_at") or "", reverse=True)
    return jsonify(data)

@app.route("/api/items/<item_id>/read", methods=["POST"])
def mark_read(item_id):
    return _update_item(item_id, read=True)

@app.route("/api/items/<item_id>/unread", methods=["POST"])
def mark_unread(item_id):
    return _update_item(item_id, read=False)

def _update_item(item_id, read):
    with lock:
        if not ITEMS_FILE.exists():
            return jsonify({"error": "not found"}), 404
        data = json.loads(ITEMS_FILE.read_text(encoding="utf-8"))
        for item in data:
            if item.get("id") == item_id:
                item["read"] = read
                ITEMS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
                return jsonify({"ok": True})
        return jsonify({"error": "not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8765, debug=False)
