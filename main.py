import json
import os
from pathlib import Path

CEIL = 200
TAG = "vnd-r3-coil"
SLOTS = {"aisle": "B4", "coil": "warm", "coin": "exact"}


def haul(panel):
    ink = panel.read_bytes()
    if ink.endswith(b"\r\n") or b"\r" in ink:
        raise SystemExit("windows line endings spotted")
    rows = [r for r in ink.decode("utf-8").split("\n") if r.strip()]
    if len(rows) != 1:
        raise SystemExit("want exactly one spoken line")
    width = len(rows[0])
    if width < 1 or width > CEIL:
        raise SystemExit(f"width {width} outside 1..{CEIL}")
    return rows[0], width


def drop(line, shell):
    shell.mkdir(parents=True, exist_ok=True)
    tag = shell / "entry.txt"
    ink = line.encode("utf-8")
    tag.write_bytes(ink)
    if tag.read_bytes() != ink:
        raise SystemExit("reel did not rewind the same")
    return tag


def main():
    root = Path(__file__).resolve().parent
    line, width = haul(root / "entry.txt")
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    shell = Path(env) if env else root / "output"
    target = drop(line, shell)
    print(json.dumps({"valid": True, "width": width, "ceiling": CEIL, "target": str(target), "aisle": SLOTS["aisle"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
