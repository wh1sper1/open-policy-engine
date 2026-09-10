import os
import json
import glob

def load_dossiers():
    dossiers = []
    files = glob.glob("dossiers/verified/*.md")
    for fpath in files:
        filename = os.path.basename(fpath)
        with open(fpath, "r", encoding="utf-8") as f:
            dossiers.append({
                "file": filename,
                "content": f.read()
            })
    return dossiers

def load_scraper_data():
    all_findings = []
    json_files = glob.glob("pipeline/scrapers/output/*.json")
    for fpath in json_files:
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    all_findings.extend(data)
        except Exception as e:
            print(f"[-] Error loading {fpath}: {e}")
    return all_findings

def build_html():
    dossiers = load_dossiers()
    findings = load_scraper_data()

    # Build Dossiers Section
    dossier_html = ""
    for d in dossiers:
        dossier_html += f"""
        <div class="card">
            <h3>📄 {d['file']}</h3>
            <pre>{d['content'][:500]}...</pre>
        </div>
        """

    # Build Global Findings Table Rows
    table_rows = ""
    for item in findings:
        table_rows += f"""
        <tr>
            <td><span class="badge">{item.get('jurisdiction', 'Global')}</span></td>
            <td>{item.get('source', 'N/A')}</td>
            <td><b>{item.get('bill_id', 'N/A')}</b></td>
            <td>{item.get('title', 'No title provided')}</td>
            <td><code>{item.get('keyword', 'N/A')}</code></td>
            <td><a href="{item.get('url', '#')}" target="_blank">View Docket</a></td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Open Policy Engine — Threat & Legislative Dashboard</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 2rem; }}
        h1 {{ color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 0.5rem; }}
        h2 {{ color: #94a3b8; margin-top: 2rem; }}
        .card {{ background: #1e293b; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; border: 1px solid #334155; }}
        pre {{ white-space: pre-wrap; word-wrap: break-word; color: #cbd5e1; background: #0f172a; padding: 1rem; border-radius: 6px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; background: #1e293b; border-radius: 8px; overflow: hidden; }}
        th, td {{ padding: 12px 16px; text-align: left; border-bottom: 1px solid #334155; }}
        th {{ background: #334155; color: #38bdf8; font-weight: 600; }}
        tr:hover {{ background: #334155; }}
        a {{ color: #38bdf8; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .badge {{ background: #0284c7; color: #fff; padding: 3px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold; }}
        code {{ background: #0f172a; padding: 2px 6px; border-radius: 4px; color: #f43f5e; }}
    </style>
</head>
<body>
    <h1>🛡️ Open Policy Engine Dashboard</h1>
    <p>Automated global legislative monitoring and verified intelligence policy dossiers.</p>

    <h2>📑 Verified Policy Dossiers ({len(dossiers)})</h2>
    {dossier_html if dossier_html else "<p>No dossiers found.</p>"}

    <h2>🌍 Live Global Scraper Monitor ({len(findings)} Records)</h2>
    <table>
        <thead>
            <tr>
                <th>Jurisdiction</th>
                <th>Source</th>
                <th>Bill / Item ID</th>
                <th>Title / Description</th>
                <th>Keyword Trigger</th>
                <th>Link</th>
            </tr>
        </thead>
        <tbody>
            {table_rows if table_rows else "<tr><td colspan='6'>No scraper findings recorded yet.</td></tr>"}
        </tbody>
    </table>
</body>
</html>
"""

    os.makedirs("docs", exist_ok=True)
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✅ Website regenerated successfully at: docs/index.html")

if __name__ == "__main__":
    build_html()