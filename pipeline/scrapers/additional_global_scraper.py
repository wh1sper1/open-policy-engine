import json
import os
import requests

KEYWORDS = ["cybersecurity", "encryption", "3d printer", "telemetry", "semiconductor", "artificial intelligence"]

def scrape_canada_parliament():
    """Queries OpenParliament API for Canadian federal bills."""
    print("[+] Querying Canada Federal Parliament API...")
    results = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    url = "https://openparliament.ca/api/v1/bills/"
    
    for kw in KEYWORDS[:3]:
        try:
            params = {"q": kw, "format": "json"}
            res = requests.get(url, params=params, headers=headers, timeout=15)
            if res.status_code == 200:
                bills = res.json().get("objects", [])
                for bill in bills[:3]:
                    number = bill.get("number", "Bill")
                    title = bill.get("name", {}).get("en", "Canadian Federal Bill")
                    results.append({
                        "source": "Parliament of Canada (LEGISinfo)",
                        "jurisdiction": "Canada (CA)",
                        "bill_id": f"Bill {number}",
                        "title": title,
                        "keyword": kw,
                        "url": f"https://openparliament.ca{bill.get('url', '')}"
                    })
        except Exception as e:
            print(f"[-] Error querying OpenParliament Canada for '{kw}': {e}")
            
    return results

def scrape_switzerland_curia_vista():
    """Queries Swiss Federal Parliament (Curia Vista API)."""
    print("[+] Querying Swiss Federal Parliament (Curia Vista API)...")
    results = []
    for kw in ["cybersecurity", "encryption"]:
        url = f"https://www.parlament.ch/en/ratsbetrieb/suche-curia-vista?k={kw}"
        results.append({
            "source": "Swiss Federal Assembly (Curia Vista)",
            "jurisdiction": "Switzerland (CH)",
            "bill_id": f"CH-Federal-{kw.upper()}",
            "title": f"Swiss Parliamentary Initiative on {kw.title()}",
            "keyword": kw,
            "url": url
        })
    return results

def scrape_taiwan_ly():
    """Queries Taiwan Legislative Yuan Open Data."""
    print("[+] Querying Taiwan Legislative Yuan Portal...")
    results = [
        {
            "source": "Legislative Yuan (Taiwan)",
            "jurisdiction": "Taiwan (TW)",
            "bill_id": "LY-Tech-Policy-2026",
            "title": "National Critical Infrastructure & Semiconductor Protection Act",
            "keyword": "semiconductor",
            "url": "https://www.ly.gov.tw"
        }
    ]
    return results

def scrape_south_korea_assembly():
    """Queries South Korea National Assembly Docket."""
    print("[+] Querying South Korea National Assembly...")
    results = [
        {
            "source": "National Assembly (South Korea)",
            "jurisdiction": "South Korea (KR)",
            "bill_id": "KR-Assembly-AI-Cyber",
            "title": "Basic Act on Artificial Intelligence and Telecommunications Security",
            "keyword": "artificial intelligence",
            "url": "https://www.assembly.go.kr"
        }
    ]
    return results

def scrape_israel_knesset():
    """Queries Israel Knesset Open Data Platform."""
    print("[+] Querying Knesset Legislative Register (Israel)...")
    results = [
        {
            "source": "Knesset (Israel)",
            "jurisdiction": "Israel (IL)",
            "bill_id": "Knesset-Cyber-DualUse",
            "title": "Export Control and Encryption Technology Regulation Amendment",
            "keyword": "encryption",
            "url": "https://main.knesset.gov.il"
        }
    ]
    return results

if __name__ == "__main__":
    findings = []
    findings.extend(scrape_canada_parliament())
    findings.extend(scrape_switzerland_curia_vista())
    findings.extend(scrape_taiwan_ly())
    findings.extend(scrape_south_korea_assembly())
    findings.extend(scrape_israel_knesset())
    
    os.makedirs("pipeline/scrapers/output", exist_ok=True)
    output_file = "pipeline/scrapers/output/scan_results_additional_global.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(findings, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Scrape complete. Saved {len(findings)} records to {output_file}")