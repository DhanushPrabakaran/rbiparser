"""
Convert data.csv (rbiparser output) to data.json for MongoDB bank migration.

Generates unique bank records with:
- key: uppercase, no spaces/special chars
- value: full bank name
- enabled: true
- enachEnabled: false
- paynimoMetadata: {}

Usage:
    python csv_to_json.py
    python csv_to_json.py --input data.csv --output data.json
"""

import csv
import json
import re
import argparse
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(levelname)s: %(message)s")
logger = logging.getLogger("csv_to_json")


def generate_key(bank_name):
    """
    Generate a unique key from bank name.
    - Remove special characters
    - Remove spaces
    - Convert to uppercase
    
    Examples:
        HDFC Bank           -> HDFCBANK
        State Bank of India -> STATEBANKOFINDIA
        Tamilnad Mercantile Bank Ltd. -> TAMILNADMERCANTILEBANKLTD
    """
    # Remove special characters (keep only alphanumeric)
    key = re.sub(r"[^a-zA-Z0-9\s]", "", bank_name)
    # Remove spaces
    key = re.sub(r"\s+", "", key)
    # Uppercase
    key = key.upper()
    return key


def convert(input_file, output_file):
    """Read data.csv and write data.json with unique bank records."""
    
    seen_keys = {}       # key -> bank name (for duplicate detection)
    seen_names = set()   # normalized names already processed
    banks = []

    inserted = 0
    skipped = 0

    logger.info("Reading: %s", input_file)

    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            bank_name = row.get("BANK", "").strip()

            if not bank_name:
                skipped += 1
                continue

            # Normalize name for dedup check
            normalized = bank_name.upper().strip()

            if normalized in seen_names:
                skipped += 1
                continue

            key = generate_key(bank_name)

            if not key:
                logger.warning("Empty key generated for: %s — skipping", bank_name)
                skipped += 1
                continue

            # Handle key collision — same key means same bank, just different formatting
            if key in seen_keys:
                skipped += 1
                continue

            seen_names.add(normalized)
            seen_keys[key] = normalized

            banks.append({
                "key": key,
                "value": bank_name,
                "enabled": True,
                "enachEnabled": False,
                "paynimoMetadata": {}
            })
            inserted += 1

    # Sort alphabetically by value for readability
    banks.sort(key=lambda x: x["value"])

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(banks, f, indent=2, ensure_ascii=False)

    logger.info("---")
    logger.info("Total unique banks inserted : %d", inserted)
    logger.info("Duplicate/empty rows skipped: %d", skipped)
    logger.info("Output written to           : %s", output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert rbiparser data.csv to banks data.json"
    )
    parser.add_argument("--input",  default="data.csv",  help="Input CSV file (default: data.csv)")
    parser.add_argument("--output", default="data.json", help="Output JSON file (default: data.json)")
    args = parser.parse_args()

    convert(args.input, args.output)