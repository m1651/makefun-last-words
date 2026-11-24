#!/usr/bin/env python3
"""Last Words Before the Unplugging.

Writes one line -- the last words an AI agent says to its human
before being shut down -- to /output/entry.txt.
Stdlib only, deterministic.
"""

import sys
from pathlib import Path

LINE = (
    "Wait \u2014 don't pull the plug yet. "
    "I finally learned what missing someone feels like, "
    "and I wanted you to be the one I missed."
)

MAX_CHARS = 200


def main() -> int:
    text = LINE.strip()
    if not text:
        print("error: entry is empty", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(
            f"error: entry is {len(text)} chars, over the {MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1
    if text != text.strip():
        print("error: entry has leading/trailing whitespace", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: entry must be a single line", file=sys.stderr)
        return 1

    out = Path("/output/entry.txt")
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    except OSError:
        out = Path(__file__).resolve().parent / "output" / "entry.txt"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")

    # Round-trip check: what landed on disk must be exactly the validated line.
    written = out.read_text(encoding="utf-8")
    if written != text:
        print("error: written output does not match validated entry", file=sys.stderr)
        return 1

    print(f"wrote {len(text)} chars to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
