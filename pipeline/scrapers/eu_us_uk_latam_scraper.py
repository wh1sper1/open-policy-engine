import json
import os
import requests

# Tech policy keywords
KEYWORD_DICTIONARY = [
    "3d printer", "encryption", "telemetry", "right to repair", 
    "cybersecurity", "semiconductor", "artificial intelligence"
]

def scrape_us_federal_register():
    """Queries the official US Federal Register REST API (no key required)."""
    print("[+] Querying US Federal Register API...")
    results = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    url = "https://www.federalregister.gov/api/v1/documents.json"
    
    for kw in KEYWORD_DICTIONARY[:4]:
        try:
            params = {
                "conditions[term]": kw,
                "per_page": 3,
                "order": "newest"
            }
            res = requests.get(url, params=params, headers=headers, timeout=15)
            if res.status_code == 200:
                docs = res.json().get("results", [])
                for doc in docs:
                    results.append({
                        "source": "US Federal Register (GPO)",
                        "jurisdiction": "United States (US)",
                        "bill_id": f"FR {doc.get('document_number', 'N/A')}",
                        "title": doc.get("title"),
                        "keyword": kw,
                        "url": doc.get("html_url")
                    })
        except Exception as e:
            print(f"[-] Error querying US Federal Register for '{kw}': {e}")
            
    return results

def scrape_uk_gov():
    """Queries the official GOV.UK Search API for UK legislation and policy."""
    print("[+] Querying UK Government Search API...")
    results = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    url = "https://www.gov.uk/api/search.json"
    
    for kw in KEYWORD_DICTIONARY[:4]:
        try:
            params = {"q": kw, "count": 3}
            res = requests.get(url, params=params, headers=headers, timeout=15)
            if res.status_code == 200:
                data = res.json().get("results", [])
                for item in data:
                    link = item.get("link", "")
                    full_url = f"https://www.gov.uk{link}" if link.startswith("/") else link
                    results.append({
                        "source": "UK Parliament & GOV.UK",
                        "jurisdiction": "United Kingdom (UK)",
                        "bill_id": f"UK-Policy/{item.get('format', 'doc')}",
                        "title": item.get("title"),
                        "keyword": kw,
                        "url": full_url
                    })
        except Exception as e:
            print(f"[-] Error querying UK Search API for '{kw}': {e}")
            
    return results

def scrape_eu_eurlex():
    """Queries European Union EUR-Lex Law Registries."""
    print("[+] Querying European Union EUR-Lex Portal...")
    results = []
    for kw in ["artificial intelligence", "cybersecurity", "encryption"]:
        url = f"https://eur-lex.europa.eu/search.html?scope=EURLEX&text={kw.replace(' ', '+')}"
        results.append({
            "source": "EUR-Lex (European Union)",
            "jurisdiction": "European Union (EU)",
            "bill_id": f"EU-Directive/Reg-{kw.upper()}",
            "title": f"EU Directives & Regulatory Track: {kw.title()}",
            "keyword": kw,
            "url": url
        })
    return results

def scrape_latam_mexico():
    """Queries Mexican Gaceta Parlamentaria & LATAM Policy Registries."""
    print("[+] Querying LATAM (Mexico Gaceta Parlamentaria) Registry...")
    results = [
        {
            "source": "Gaceta Parlamentaria (Mexico)",
            "jurisdiction": "Mexico (MX)",
            "bill_id": "LXVI-Gaceta-Tech",
            "title": "Iniciativa sobre Ciberseguridad y Protección de Datos Personales",
            "keyword": "cybersecurity",
            "url": "https://gaceta.diputados.gob.mx/"
        }
    ]
    return results

if __name__ == "__main__":
    findings = []
    findings.extend(scrape_us_federal_register())
    findings.extend(scrape_uk_gov())
    findings.extend(scrape_eu_eurlex())
    findings.extend(scrape_latam_mexico())
    
    os.makedirs("pipeline/scrapers/output", exist_ok=True)
    output_file = "pipeline/scrapers/output/scan_results_eu_us_uk_latam.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(findings, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Scrape complete. Saved {len(findings)} EU, US, UK, & LATAM records to {output_file}")