import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from unisdb.db import connect, read_local_secrets  # noqa: E402
from unisdb.text import compact  # noqa: E402

JSON_FILE = ROOT / "data" / "societies.json"
TYPES = {"universidad", "escolar", "independiente"}


def validate(records: list[dict]) -> list[str]:
    errors, seen = [], {}
    for r in records:
        where = f"row {r.get('source_row')} ({r.get('code') or 'no code'})"
        if not r.get("code"):
            errors.append(f"{where}: missing code")
        elif compact(r["code"]) in seen:
            errors.append(f"{where}: code clashes with {seen[compact(r['code'])]}")
        else:
            seen[compact(r["code"])] = r["code"]
        if r.get("type") not in TYPES:
            errors.append(f"{where}: type must be one of {sorted(TYPES)}, got {r.get('type')!r}")
        if not r.get("society", {}).get("name"):
            errors.append(f"{where}: missing society name")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--replace", action="store_true", help="Delete existing societies before loading")
    args = parser.parse_args()

    records = json.loads(JSON_FILE.read_text(encoding="utf-8"))
    errors = validate(records)
    if errors:
        sys.exit("Fix these in the JSON first:\n- " + "\n- ".join(errors))

    secrets = read_local_secrets()["mongo"]
    collection = connect(secrets["uri"], secrets["db"])["societies"]

    existing = collection.count_documents({})
    if existing and not args.replace:
        sys.exit(f"'societies' already has {existing} documents. Use --replace to wipe and reload.")
    if args.replace:
        collection.delete_many({})

    collection.create_index("code", unique=True)
    collection.insert_many(records)
    print(f"Loaded {len(records)} societies into {secrets['db']}.societies")


if __name__ == "__main__":
    main()