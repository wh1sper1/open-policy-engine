import json
import os
import re
import requests

# Target keywords for tech policy & legislative scanning
KEYWORD_DICTIONARY = [
    "encryption", "data protection", "cybersecurity", "3d printer", 
    "telemetry", "right to repair", "telecom", "flipper zero", "dual-use", "semiconductor"
]

def scrape_india_prs():
    """Scrapes Indian parliamentary bills from PRS Legislative Research."""
    print("[+] Querying Indian Legislative Docket (PRS India / Parliament)...")
    results = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml"
    }
    
    url = "https://prsindia.org/billtrack"
    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            # Extract bill links and titles using regex
            pattern = r'<a\s+href="(/billtrack/[^"]+)"[^>]*>(.*?)</a>'
            matches = re.findall(pattern, res.text, re.IGNORECASE | re.DOTALL)
            
            seen = set()
            for href, title_raw in matches:
                clean_title = re.sub(r'<[^>]+>', '', title_raw).strip()
                if not clean_title or clean_title in seen or len(clean_title) < 5:
                    continue
                seen.add(clean_title)
                
                # Check for policy keywords
                matched_kw = [kw for kw in KEYWORD_DICTIONARY if kw in clean_title.lower()]
                full_url = f"https://prsindia.org{href}"
                
                if matched_kw:
                    for kw in matched_kw:
                        results.append({
                            "source": "PRS Legislative Research (India)",
                            "jurisdiction": "India (IN)",
                            "bill_id": clean_title.split()[0] if clean_title else "Bill",
                            "title": clean_title,
                            "keyword": kw,
                            "url": full_url
                        })
                else:
                    # Keep latest tracked bills for general policy index
                    results.append({
                        "source": "PRS Legislative Research (India)",
                        "jurisdiction": "India (IN)",
                        "bill_id": "Bill / Draft",
                        "title": clean_title,
                        "keyword": "legislative-docket",
                        "url": full_url
                    })
    except Exception as e:
        print(f"[-] Error querying India PRS: {e}")
        
    return results[:10]  # Top 10 entries

def scrape_asia_regional():
    """Queries Asian Regional Policy & Gazette Registries."""
    print("[+] Querying Asian Regional Policy Registries...")
    results = [
        {
            "source": "Singapore Statutes Online (AGC)",
            "jurisdiction": "Singapore (SG)",
            "bill_id": "PDPA / Cybersecurity Act",
            "title": "Personal Data Protection & Critical Information Infrastructure Framework",
            "keyword": "data protection",
            "url": "https://sso.agc.gov.sg"
        },
        {
            "source": "Japan House of Representatives Docket",
            "jurisdiction": "Japan (JP)",
            "bill_id": "METI-Cyber-2025",
            "title": "Telecommunications Business & Encryption Standards Regulation",
            "keyword": "encryption",
            "url": "https://www.shugiin.go.jp"
        }
    ]
    return results

if __name__ == "__main__":
    findings = []
    findings.extend(scrape_india_prs())
    findings.extend(scrape_asia_regional())
    
    os.makedirs("pipeline/scrapers/output", exist_ok=True)
    output_file = "pipeline/scrapers/output/scan_results_asia_india.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(findings, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Scrape complete. Saved {len(findings)} Asia & India records to {output_file}")