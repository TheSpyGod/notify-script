import sys
import json
import requests
from pathlib import Path

config = json.loads((Path(__file__).parent / "config.json").read_text())

if len(sys.argv) < 2:
    print("Usage: notify.py <message>")
    sys.exit(1)

requests.post(config["url"], data=sys.argv[1], timeout=5)
