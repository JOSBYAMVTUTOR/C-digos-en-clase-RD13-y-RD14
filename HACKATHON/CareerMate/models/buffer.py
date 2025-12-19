import json
from pathlib import Path
from datetime import datetime
from typing import List

BUFFER_FILE = Path("models/artifacts/buffer.jsonl")


def add_to_buffer(features: List[float], labels: List[str]) -> None:
    BUFFER_FILE.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "features": [float(x) for x in features],
        "labels": labels,
    }

    with BUFFER_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def load_buffer():
    if not BUFFER_FILE.exists():
        return []

    with BUFFER_FILE.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def clear_buffer():
    if BUFFER_FILE.exists():
        BUFFER_FILE.unlink()