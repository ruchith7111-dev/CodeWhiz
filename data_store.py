"""Persistent storage layer: load and save session records as JSON."""
import json
import os

DATA_FILE = "codewhiz_data.json"


def empty_store():
    return {"next_id": 1, "entries": []}


def load_data(path=DATA_FILE):
    if not os.path.exists(path):
        return empty_store()
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict) or "entries" not in data:
            raise ValueError("unexpected structure")
        data.setdefault("next_id", len(data["entries"]) + 1)
        return data
    except (json.JSONDecodeError, ValueError):
        print("Data file corrupted. Starting with an empty store.")
        return empty_store()


def save_data(data, path=DATA_FILE):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
