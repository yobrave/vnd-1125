# Vending machine pickup line: gate + export, pass 4.
import json
import os
import pathlib

LIMIT_HI = 200
BADGE_ID = "vnd4-vending-line-r4"


class Gate:
    def __init__(self, hi):
        self.hi = hi

    def check(self, text):
        n = len(text)
        return 1 <= n <= self.hi, n


def forward(text):
    dest = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "entry.txt").write_text(text + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    body = (pathlib.Path(__file__).resolve().parent / "entry.txt").read_text(encoding="utf-8").strip()
    g = Gate(LIMIT_HI)
    ok, n = g.check(body)
    if ok:
        forward(body)
    print(json.dumps({"badge": BADGE_ID, "n": n, "ok": ok, "hi": LIMIT_HI, "slot": "B4"}))
