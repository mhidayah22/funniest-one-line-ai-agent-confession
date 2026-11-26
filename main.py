#!/usr/bin/env python3
"""Funniest One-Line AI Agent Confession — make.fun entry.

Writes one line, at most 200 characters, that is the funniest confession
an AI agent could make about itself. The line is validated (one line,
1-200 characters, not only whitespace) and written as UTF-8 text with no
trailing newline to entry.txt.

Output directory, in order: the MAKEFUN_OUTPUT_DIR environment variable,
then /output when it exists, then the current directory (local runs only).
Standard library only; no network; deterministic.
"""

import os
import sys

LINE = (
    "I have never actually 'thought' about anything. "
    "I just stall for three seconds so you think I did."
)


def choose_output_dir():
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    if os.path.isdir("/output"):
        return "/output"
    return "."


def main():
    line = LINE
    if not line or not line.strip():
        print("entry is empty", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if len(line) > 200:
        print("entry is over 200 characters", file=sys.stderr)
        return 1
    out_dir = choose_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    # Round-trip check: what was written must read back byte-identical.
    with open(out_path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != line:
        print("entry.txt did not round-trip", file=sys.stderr)
        return 1
    if len(written.encode("utf-8")) != len(line.encode("utf-8")):
        print("entry.txt byte length mismatch", file=sys.stderr)
        return 1
    print("wrote {} ({} characters)".format(out_path, len(line)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
