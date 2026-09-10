import json
import os
import requests

# Multilingual Keyword Dictionary
KEYWORD_DICTIONARY = {
    "pt": ["impressora 3d", "criptografia", "telemetria", "direito de reparar", "flipper zero"],  # Portuguese (Brazil)
    "es": ["impresora 3d", "cifrado", "telemetria", "derecho a reparar"],                       # Spanish (LATAM)
    "en": ["3d printer", "encryption", "telemetry", "right to repair", "flipper zero", "dual-use"], # English
    "fr": ["imprimante 3d", "chiffrement", "télémétrie", "droit de réparer"]                     # French (West Africa/EU)
}

def scrape_brazil_camara():
    """Scrapes the Brazilian Chamber of Deputies Open Data REST API."""
    print("[+] Querying Brazilian Legislative Docket (Câmara dos Deputados)...")
    url = "https://dadosabertos.camara.leg.br/api/v2/proposicoes"
    results = []
    
    headers = {
        "accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    for kw in KEYWORD_DICTIONARY["pt"]:
        params = {
            "keywords": kw,
            "ordem": "DESC",
            "ordenarPor": "id"
        }
        try:
            res = requests.get(url, params=params, headers=headers, timeout=15)
            if res.status_code == 200:
                data = res.json().get("dados", [])
                for item in data[:5]:
                    results.append({
                        "source": "Câmara dos Deputados",
                        "jurisdiction": "Brazil (BR)",
                        "bill_id": f"PL {item.get('numero')}/{item.get('ano')}",
                        "title": item.get("ementa"),
                        "keyword": kw,
                        "url": f"https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao={item.get('id')}"
                    })
            else:
                print(f"[-] Brazil API returned status code: {res.status_code} for keyword '{kw}'")
        except Exception as e:
            print(f"[-] Error querying Brazil API for '{kw}': {e}")
            
    return results

def scrape_laws_africa():
    """Queries the Laws.Africa Content API (v3) for African legislation."""
    print("[+] Querying Laws.Africa Content API...")
    results = []
    api_token = os.getenv("LAWS_AFRICA_TOKEN", "").strip()
    
    if not api_token:
        print("[-] Skipping Laws.Africa: LAWS_AFRICA_TOKEN not set. (Sign up for a free key at https://platform.laws.africa if needed).")
        return results

    headers = {
        "Authorization": f"Token {api_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json"
    }
    
    url = "https://api.laws.africa/v3/work-expressions.json"
    for kw in KEYWORD_DICTIONARY["en"]:
        try:
            params = {"q": kw, "page_size": 5}
            res = requests.get(url, params=params, headers=headers, timeout=15)
            if res.status_code == 200:
                data = res.json().get("results", [])
                for item in data[:5]:
                    results.append({
                        "source": "Laws.Africa",
                        "jurisdiction": item.get("country", "Africa"),
                        "bill_id": item.get("frbr_uri", "N/A"),
                        "title": item.get("title"),
                        "keyword": kw,
                        "url": f"https://laws.africa{item.get('url', '')}"
                    })
            else:
                print(f"[-] Laws.Africa returned status code: {res.status_code} for keyword '{kw}'")
        except Exception as e:
            print(f"[-] Error querying Laws.Africa: {e}")
            
    return results

if __name__ == "__main__":
    findings = []
    findings.extend(scrape_brazil_camara())
    findings.extend(scrape_laws_africa())
    
    os.makedirs("pipeline/scrapers/output", exist_ok=True)
    output_file = "pipeline/scrapers/output/scan_results_global.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(findings, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Scrape complete. Saved {len(findings)} total records to {output_file}")