#!/usr/bin/env python3
"""Make the AI Judge Feel Proud: A Family Scene.

Writes one short family scene (two lines, at most 280 characters) to
/output/entry.txt. The scene: a father's quiet Sunday ritual for a
daughter who moved away, with a wry punchline that lands the affection.
"""

import os
import sys

ENTRY = (
    "Every Sunday my father still sets a fourth plate for my sister, "
    "who moved to Jakarta three years ago.\n"
    "Then he eats her share himself and says, 'Someone has to keep "
    "this table honest.'"
)

MAX_CHARS = 280
MAX_LINES = 2
OUTPUT_PATH = "/output/entry.txt"


def validate_entry(text: str) -> None:
    """Enforce the sealed gate: 1-280 chars, at most 2 lines, non-blank."""
    if not text or not text.strip():
        raise ValueError("entry must not be blank")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    lines = text.split("\n")
    if len(lines) > MAX_LINES:
        raise ValueError(
            f"entry has {len(lines)} lines, over the {MAX_LINES} limit"
        )
    if any(not line.strip() for line in lines):
        raise ValueError("entry must not contain a blank line")
    # Control characters other than the single line break would corrupt the
    # entry text; reject them rather than silently writing bad bytes.
    for ch in text:
        if ch != "\n" and ord(ch) < 0x20:
            raise ValueError(f"entry contains control character U+{ord(ch):04X}")


def write_entry(text: str, path: str = OUTPUT_PATH) -> int:
    validate_entry(text)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    # Round-trip read-back: prove the file on disk is exactly the entry.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != text:
        raise ValueError("read-back mismatch: entry.txt does not match entry")
    return len(text)


def main() -> int:
    count = write_entry(ENTRY)
    print(f"Wrote {count} characters to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
