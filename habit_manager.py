"""Core operations on coding session records (add, update, delete, filter)."""
from datetime import date

CATEGORIES = ["DSA", "Web", "AI/ML", "Debugging", "Projects", "Other"]


def add_entry(data, language, category, hours, notes=""):
    if hours < 0:
        raise ValueError("hours must be non-negative")
    entry = {
        "id": data["next_id"],
        "date": date.today().isoformat(),
        "language": language,
        "category": category,
        "hours": float(hours),
        "notes": notes,
    }
    data["entries"].append(entry)
    data["next_id"] += 1
    return entry


def get_entry(data, entry_id):
    for entry in data["entries"]:
        if entry["id"] == entry_id:
            return entry
    return None


def update_entry(data, entry_id, **changes):
    entry = get_entry(data, entry_id)
    if entry is None:
        return False
    for key, value in changes.items():
        if key in entry and value not in (None, ""):
            entry[key] = float(value) if key == "hours" else value
    return True


def delete_entry(data, entry_id):
    before = len(data["entries"])
    data["entries"] = [e for e in data["entries"] if e["id"] != entry_id]
    return len(data["entries"]) < before


def filter_entries(data, category=None, language=None):
    result = data["entries"]
    if category:
        result = [e for e in result if e["category"] == category]
    if language:
        result = [e for e in result if e["language"].lower() == language.lower()]
    return result
