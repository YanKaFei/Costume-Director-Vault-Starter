#!/usr/bin/env python3
"""Generate the repository mirror skill from the canonical .dsh skill.

Canonical: .dsh/skills/costume-director/SKILL.md
Mirror:    skills/costume-director/SKILL.md (DO-NOT-EDIT, deterministic)

Usage: python3 scripts/sync_skill.py --write|--check [--json]
Exit 0 match/write ok; 1 drift (check only); 2 missing canonical.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / ".dsh/skills/costume-director/SKILL.md"
MIRROR = ROOT / "skills/costume-director/SKILL.md"
HEADER = ("<!-- DO NOT EDIT: generated from .dsh/skills/costume-director/SKILL.md "
          "by scripts/sync_skill.py -->")


def generate():
    if not CANONICAL.exists():
        raise FileNotFoundError(str(CANONICAL))
    body = CANONICAL.read_text(encoding="utf-8")
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    return (HEADER + "\n<!-- source-sha256: %s -->\n" % digest + body)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        generated = generate()
    except FileNotFoundError as exc:
        print("ERROR: canonical skill missing: %s" % exc, file=sys.stderr)
        return 2
    if args.write:
        MIRROR.parent.mkdir(parents=True, exist_ok=True)
        MIRROR.write_text(generated, encoding="utf-8")
        print(json.dumps({"status": "written", "path": str(MIRROR)}) if args.json
              else "wrote %s" % MIRROR)
        return 0
    current = MIRROR.read_text(encoding="utf-8") if MIRROR.exists() else ""
    match = current == generated
    if args.json:
        print(json.dumps({"status": "match" if match else "drift",
                          "canonical": str(CANONICAL), "mirror": str(MIRROR)}))
    else:
        print("MATCH" if match else "DRIFT")
    return 0 if match else 1


if __name__ == "__main__":
    sys.exit(main())
