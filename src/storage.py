import json

def save_to_jsonl(data, filename="discovery_log.jsonl"):
    """
    Appends data to a JSON Lines file.
    """
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")