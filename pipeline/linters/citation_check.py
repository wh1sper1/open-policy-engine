#!/usr/bin/env python3
import sys
import re
from pathlib import Path

LOW_WEIGHT_DOMAINS = ["youtube.com", "youtu.be", "twitter.com", "x.com", "tiktok.com", "medium.com"]
TAXONOMY_PATTERN = re.compile(r"\[(VERIFIED|PLAUSIBLE|ALLEGED)\]", re.IGNORECASE)
LINK_PATTERN = re.compile(r"\[([^\]]+)\]\((https?://[^\s\)]+)\)")

def lint_file(file_path):
    errors = []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for idx, line in enumerate(lines, 1):
        tax_match = TAXONOMY_PATTERN.search(line)
        links = LINK_PATTERN.findall(line)
        if tax_match:
            tag = tax_match.group(1).upper()
            if tag in ["VERIFIED", "PLAUSIBLE"] and not links:
                errors.append(f"Line {idx}: [{tag}] claim missing inline primary source link.")
            elif tag == "VERIFIED":
                for _, url in links:
                    if any(domain in url.lower() for domain in LOW_WEIGHT_DOMAINS):
                        errors.append(f"Line {idx}: [{tag}] claim uses invalid domain ({url}).")
    return errors

def main():
    target_dirs = ["dossiers", "vectors"]
    total_errors = 0
    for d in target_dirs:
        for filepath in Path(d).glob("**/*.md"):
            errors = lint_file(filepath)
            for e in errors:
                print(f"❌ ERROR ({filepath}): {e}")
                total_errors += 1
    if total_errors > 0:
        sys.exit(1)
    print("✅ Citation check passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
