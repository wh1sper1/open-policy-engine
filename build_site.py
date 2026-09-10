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
    return all_findings, len(json_files)

def build_html():
    dossiers = load_dossiers()
    findings, pipeline_count = load_scraper_data()

    # Calculate live stats
    jurisdictions = sorted(list(set(item.get("jurisdiction", "Global") for item in findings)))
    total_findings = len(findings)
    total_dossiers = len(dossiers)

    # Build Dossier Cards
    dossier_html = ""
    for d in dossiers:
        dossier_html += f"""
        <div class="dossier-card">
            <div class="dossier-header">
                <span class="dossier-badge">VERIFIED DOSSIER</span>
                <h3>{d['file']}</h3>
            </div>
            <pre>{d['content'][:450]}...</pre>
        </div>
        """

    # Build Table Rows & Jurisdiction Filter Options
    table_rows = ""
    for item in findings:
        jur = item.get('jurisdiction', 'Global')
        table_rows += f"""
        <tr data-jurisdiction="{jur}">
            <td><span class="badge">{jur}</span></td>
            <td class="source-cell">{item.get('source', 'N/A')}</td>
            <td><code class="bill-id">{item.get('bill_id', 'N/A')}</code></td>
            <td class="title-cell">{item.get('title', 'No title provided')}</td>
            <td><span class="kw-tag">{item.get('keyword', 'N/A')}</span></td>
            <td><a href="{item.get('url', '#')}" target="_blank" class="action-btn">View Docket ↗</a></td>
        </tr>
        """

    jur_options = "".join([f'<option value="{j}">{j}</option>' for j in jurisdictions])

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PolicyHorizon — Global Tech & Hardware Intelligence Radar</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-main: #0b0f19;
            --bg-card: #151d2a;
            --bg-hover: #1e293b;
            --border-color: #27354a;
            --primary-accent: #38bdf8;
            --primary-glow: rgba(56, 189, 248, 0.15);
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --tag-bg: #0f172a;
            --badge-bg: #0284c7;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-main);
            color: var(--text-main);
            padding: 2rem 3rem;
            line-height: 1.5;
        }}

        header {{
            margin-bottom: 2rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}

        .brand h1 {{
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--text-main);
            letter-spacing: -0.02em;
        }}

        .brand h1 span {{ color: var(--primary-accent); }}
        .brand p {{ color: var(--text-muted); font-size: 0.95rem; margin-top: 0.25rem; }}

        /* Metrics Bar */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2.5rem;
        }}

        .metric-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1.25rem;
        }}

        .metric-card .num {{
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--primary-accent);
        }}

        .metric-card .label {{
            font-size: 0.85rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 0.2rem;
        }}

        /* Section Styling */
        section {{ margin-bottom: 3rem; }}
        h2 {{ font-size: 1.3rem; font-weight: 600; margin-bottom: 1rem; color: var(--text-main); display: flex; align-items: center; gap: 0.5rem; }}

        /* Dossiers Grid */
        .dossiers-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
            gap: 1.25rem;
        }}

        .dossier-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1.25rem;
            transition: border-color 0.2s, transform 0.2s;
        }}

        .dossier-card:hover {{
            border-color: var(--primary-accent);
            transform: translateY(-2px);
        }}

        .dossier-badge {{
            background: rgba(16, 185, 129, 0.15);
            color: #10b981;
            font-size: 0.7rem;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 4px;
            letter-spacing: 0.05em;
        }}

        .dossier-card h3 {{ font-size: 1rem; margin-top: 0.5rem; margin-bottom: 0.75rem; color: var(--text-main); }}
        .dossier-card pre {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem;
            color: #cbd5e1;
            background: #0b0f19;
            padding: 0.85rem;
            border-radius: 6px;
            white-space: pre-wrap;
            max-height: 180px;
            overflow-y: auto;
        }}

        /* Search & Controls */
        .controls-bar {{
            display: flex;
            gap: 1rem;
            margin-bottom: 1.25rem;
            flex-wrap: wrap;
        }}

        .search-input, .select-filter {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 0.65rem 1rem;
            border-radius: 8px;
            font-size: 0.9rem;
            outline: none;
            transition: border-color 0.2s;
        }}

        .search-input {{ flex: 1; min-width: 260px; }}
        .search-input:focus, .select-filter:focus {{ border-color: var(--primary-accent); box-shadow: 0 0 0 3px var(--primary-glow); }}

        /* Radar Table */
        .table-container {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}

        table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem; }}
        th {{
            background: #1a2332;
            color: var(--text-muted);
            font-weight: 600;
            padding: 14px 18px;
            border-bottom: 1px solid var(--border-color);
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
        }}

        td {{ padding: 14px 18px; border-bottom: 1px solid var(--border-color); color: var(--text-main); }}
        tr:last-child td {{ border-bottom: none; }}
        tr:hover td {{ background: var(--bg-hover); }}

        .badge {{
            background: var(--badge-bg);
            color: #fff;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            white-space: nowrap;
        }}

        .bill-id {{
            font-family: 'JetBrains Mono', monospace;
            background: #0f172a;
            color: var(--primary-accent);
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.82rem;
            border: 1px solid var(--border-color);
        }}

        .kw-tag {{
            background: rgba(244, 63, 94, 0.15);
            color: #f43f5e;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 500;
            border: 1px solid rgba(244, 63, 94, 0.3);
        }}

        .action-btn {{
            color: var(--primary-accent);
            text-decoration: none;
            font-weight: 500;
            font-size: 0.85rem;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            transition: color 0.15s;
        }}

        .action-btn:hover {{ color: #7dd3fc; text-decoration: underline; }}
        .source-cell {{ max-width: 180px; }}
        .title-cell {{ max-width: 380px; line-height: 1.4; }}
    </style>
</head>
<body>

    <header>
        <div class="brand">
            <h1>Policy<span>Horizon</span></h1>
            <p>Global Technology & Dual-Use Hardware Regulatory Intelligence</p>
        </div>
    </header>

    <div class="metrics-grid">
        <div class="metric-card">
            <div class="num">{total_findings}</div>
            <div class="label">Live Scraped Docket Items</div>
        </div>
        <div class="metric-card">
            <div class="num">{len(jurisdictions)}</div>
            <div class="label">Jurisdictions Monitored</div>
        </div>
        <div class="metric-card">
            <div class="num">{total_dossiers}</div>
            <div class="label">Verified Intelligence Dossiers</div>
        </div>
        <div class="metric-card">
            <div class="num">{pipeline_count}</div>
            <div class="label">Active Scraper Pipelines</div>
        </div>
    </div>

    <section>
        <h2>📑 Verified Policy Dossiers</h2>
        <div class="dossiers-grid">
            {dossier_html if dossier_html else "<p style='color:var(--text-muted);'>No verified dossiers loaded.</p>"}
        </div>
    </section>

    <section>
        <h2>🌍 Global Legislative Radar</h2>
        
        <div class="controls-bar">
            <input type="text" id="searchInput" class="search-input" onkeyup="filterRadar()" placeholder="⚡ Search by keyword, title, bill ID, or source...">
            <select id="jurisdictionFilter" class="select-filter" onchange="filterRadar()">
                <option value="ALL">All Jurisdictions ({len(jurisdictions)})</option>
                {jur_options}
            </select>
        </div>

        <div class="table-container">
            <table id="radarTable">
                <thead>
                    <tr>
                        <th>Jurisdiction</th>
                        <th>Source</th>
                        <th>Bill / Item ID</th>
                        <th>Title / Summary</th>
                        <th>Trigger Keyword</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows if table_rows else "<tr><td colspan='6' style='text-align:center;'>No scraper data available.</td></tr>"}
                </tbody>
            </table>
        </div>
    </section>

    <script>
        function filterRadar() {{
            const searchVal = document.getElementById('searchInput').value.toLowerCase();
            const jurVal = document.getElementById('jurisdictionFilter').value;
            const rows = document.querySelectorAll('#radarTable tbody tr');

            rows.forEach(row => {{
                const text = row.innerText.toLowerCase();
                const rowJur = row.getAttribute('data-jurisdiction');
                
                const matchesSearch = text.includes(searchVal);
                const matchesJur = (jurVal === 'ALL' || rowJur === jurVal);

                if (matchesSearch && matchesJur) {{
                    row.style.display = '';
                }} else {{
                    row.style.display = 'none';
                }}
            }});
        }}
    </script>

</body>
</html>
"""

    os.makedirs("docs", exist_ok=True)
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✅ PolicyHorizon dashboard rebuilt successfully at: docs/index.html")

if __name__ == "__main__":
    build_html()