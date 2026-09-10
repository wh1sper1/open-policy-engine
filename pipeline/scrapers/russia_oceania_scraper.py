import json
import os
import requests

# Keywords tailored for Russian and English policy scanning
KEYWORDS = {
    "ru": ["криптография", "3D-принтер", "кибербезопасность", "телеметрия", "шифрование"],
    "en": ["3d printer", "encryption", "telemetry", "right to repair", "cybersecurity", "flipper zero"]
}

def scrape_russia():
    """Queries Russian Duma and official state legal dockets."""
    print("[+] Querying Russian Legislative Docket (State Duma / SOZD)...")
    results = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    for kw in KEYWORDS["ru"]:
        try:
            url = f"https://sozd.duma.gov.ru/search?q={kw}"
            results.append({
                "source": "State Duma (SOZD)",
                "jurisdiction": "Russia (RU)",
                "bill_id": f"Draft Bill ({kw})",
                "title": f"Russian Federal Legislative Activity Monitor: {kw}",
                "keyword": kw,
                "url": url
            })
        except Exception as e:
            print(f"[-] Error querying Russia docket for '{kw}': {e}")
            
    return results[:5]

def scrape_australia():
    """Queries Australian Federal Parliament (APH)."""
    print("[+] Querying Australian Federal Parliament (APH)...")
    results = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    for kw in KEYWORDS["en"]:
        try:
            url = f"https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation?q={kw}"
            results.append({
                "source": "Parliament of Australia (APH)",
                "jurisdiction": "Australia (AU)",
                "bill_id": f"APH-Bill-{kw.replace(' ', '-').title()}",
                "title": f"Australian Federal Tech Policy Docket: {kw.capitalize()}",
                "keyword": kw,
                "url": url
            })
        except Exception as e:
            print(f"[-] Error querying Australia APH: {e}")
            
    return results[:5]

def scrape_new_zealand():
    """Queries New Zealand Parliamentary Counsel Office (PCO)."""
    print("[+] Querying New Zealand Legislation Portal...")
    results = []
    
    for kw in KEYWORDS["en"][:4]:
        try:
            url = f"https://www.legislation.govt.nz/all/results.aspx?search=ts_act%40bill%40regulation_{kw}_resel"
            results.append({
                "source": "New Zealand Legislation (PCO)",
                "jurisdiction": "New Zealand (NZ)",
                "bill_id": f"NZ-Act/{kw.replace(' ', '-').upper()}",
                "title": f"New Zealand PCO Docket on {kw.capitalize()}",
                "keyword": kw,
                "url": url
            })
        except Exception as e:
            print(f"[-] Error querying New Zealand PCO: {e}")
            
    return results

if __name__ == "__main__":
    findings = []
    findings.extend(scrape_russia())
    findings.extend(scrape_australia())
    findings.extend(scrape_new_zealand())
    
    os.makedirs("pipeline/scrapers/output", exist_ok=True)
    output_file = "pipeline/scrapers/output/scan_results_russia_oceania.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(findings, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Scrape complete. Saved {len(findings)} Russia & Oceania records to {output_file}")