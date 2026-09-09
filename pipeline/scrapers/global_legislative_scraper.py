#!/usr/bin/env python3
"""
Global Legislative Scraper Pipeline
Open Policy Engine

Scrapes active policy developments across:
1. All 50 US States (Open States API v3)
2. US Federal (Congress.gov API)
3. UK Parliament (UK Parliament Bills API)
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path

# Keywords defining policy engine vectors
SEARCH_KEYWORDS = [
    "encryption",
    "3D printer",
    "additive manufacturing",
    "telemetry",
    "dual-use",
    "right to repair",
    "driver monitoring"
]

OUTPUT_DIR = Path("pipeline/scrapers/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class GlobalPolicyScraper:
    def __init__(self):
        self.openstates_key = os.getenv("OPENSTATES_API_KEY", "")
        self.congress_key = os.getenv("CONGRESS_API_KEY", "")
        self.results = []

    def scrape_us_states(self):
        """Scrapes legislative bills across all 50 US states via OpenStates v3."""
        print("🔍 Querying US States (All 50 States)...")
        if not self.openstates_key:
            print("  ⚠️ Skipping OpenStates: OPENSTATES_API_KEY environment variable not set.")
            return

        headers = {"X-API-KEY": self.openstates_key}
        for kw in SEARCH_KEYWORDS:
            url = f"https://v3.openstates.org/bills?q={kw}&page=1&per_page=10"
            try:
                resp = requests.get(url, headers=headers, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    for bill in data.get("results", []):
                        self.results.append({
                            "source": "US State",
                            "jurisdiction": bill.get("jurisdiction", {}).get("name", "State"),
                            "bill_id": bill.get("identifier"),
                            "title": bill.get("title"),
                            "keyword": kw,
                            "url": bill.get("openstates_url")
                        })
            except Exception as e:
                print(f"  ❌ Failed US States query for '{kw}': {e}")

    def scrape_us_federal(self):
        """Scrapes US Federal bills via api.congress.gov."""
        print("🔍 Querying US Federal Congress...")
        if not self.congress_key:
            print("  ⚠️ Skipping US Federal: CONGRESS_API_KEY environment variable not set.")
            return

        for kw in SEARCH_KEYWORDS:
            url = f"https://api.congress.gov/v3/bill?q={kw}&api_key={self.congress_key}&format=json&limit=5"
            try:
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    for bill in data.get("bills", []):
                        self.results.append({
                            "source": "US Federal",
                            "jurisdiction": "US Federal",
                            "bill_id": f"{bill.get('type')}{bill.get('number')}",
                            "title": bill.get("title"),
                            "keyword": kw,
                            "url": bill.get("url")
                        })
            except Exception as e:
                print(f"  ❌ Failed US Federal query for '{kw}': {e}")

    def scrape_uk_parliament(self):
        """Scrapes UK Parliament bills via public UK Bills API."""
        print("🔍 Querying UK Parliament...")
        base_url = "https://bills-api.parliament.uk/api/v1/Bills"
        for kw in SEARCH_KEYWORDS:
            try:
                resp = requests.get(base_url, params={"SearchTerm": kw, "take": 5}, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    for item in data.get("items", []):
                        bill = item.get("value", {})
                        self.results.append({
                            "source": "International (UK)",
                            "jurisdiction": "United Kingdom",
                            "bill_id": f"UK-BILL-{bill.get('billId')}",
                            "title": bill.get("shortTitle"),
                            "keyword": kw,
                            "url": f"https://bills.parliament.uk/bills/{bill.get('billId')}"
                        })
            except Exception as e:
                print(f"  ❌ Failed UK Parliament query for '{kw}': {e}")

    def run_all(self):
        print("🚀 Executing Global Policy Scraper Pipeline...")
        self.scrape_us_states()
        self.scrape_us_federal()
        self.scrape_uk_parliament()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_file = OUTPUT_DIR / f"scan_results_{timestamp}.json"
        out_file.write_text(json.dumps(self.results, indent=2), encoding="utf-8")
        
        print(f"\n✅ Scan Complete. {len(self.results)} total findings written to: {out_file}")


if __name__ == "__main__":
    scraper = GlobalPolicyScraper()
    scraper.run_all()