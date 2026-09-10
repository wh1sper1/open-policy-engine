import json
import glob
from pathlib import Path

# Ensure docs directory exists for GitHub Pages
docs_dir = Path("docs")
docs_dir.mkdir(exist_ok=True)

# Gather all scraper outputs
scan_files = glob.glob("pipeline/scrapers/output/scan_results_*.json")
all_findings = []

for sf in scan_files:
    try:
        with open(sf, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_findings.extend(data)
    except Exception:
        pass

# Deduplicate findings by title/url
unique_findings = []
seen = set()
for item in all_findings:
    identifier = item.get("url") or item.get("title")
    if identifier and identifier not in seen:
        seen.add(identifier)
        unique_findings.append(item)

findings_json = json.dumps(unique_findings)

html_content = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Open Policy Engine | Global Threat Radar</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        brand: {{
                            50: '#f0fdf4',
                            500: '#22c55e',
                            900: '#14532d',
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased min-h-screen flex flex-col">

    <!-- Navigation -->
    <nav class="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <i class="fa-solid fa-[#00ff66] fa-shield-halved text-emerald-400 text-2xl"></i>
                <span class="font-bold text-xl tracking-wider text-slate-100">OPEN<span class="text-emerald-400">POLICY</span>ENGINE</span>
            </div>
            <div class="flex space-x-6 text-sm font-medium">
                <a href="#radar" class="hover:text-emerald-400 transition">Early Warning Radar</a>
                <a href="#feeds" class="hover:text-emerald-400 transition">Threat Feeds</a>
                <a href="#dossiers" class="hover:text-emerald-400 transition">Verified Dossiers</a>
                <a href="#submit" class="bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded-md transition">Submit Intelligence</a>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <header class="border-b border-slate-800 bg-gradient-to-b from-slate-900 to-slate-950 py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-emerald-500/30 bg-emerald-500/10 text-emerald-400 text-xs font-semibold mb-6">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span> Live Global Surveillance Engine
            </div>
            <h1 class="text-4xl sm:text-6xl font-extrabold text-white tracking-tight">
                Defending Technical Sovereignty & User Agency
            </h1>
            <p class="mt-4 text-lg text-slate-400 max-w-3xl">
                Automated policy intelligence tracking legislative bills, court precedents, and vendor TOS changes across 50 US States, Federal Courts, UK Parliament, and the European Union.
            </p>
            <div class="mt-8 flex flex-wrap gap-4">
                <a href="#radar" class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold px-6 py-3 rounded-lg shadow-lg shadow-emerald-500/20 transition">
                    Explore Threat Radar
                </a>
                <a href="https://github.com/wh1sper1/open-policy-engine" target="_blank" class="border border-slate-700 bg-slate-900 hover:bg-slate-800 text-slate-200 font-semibold px-6 py-3 rounded-lg transition flex items-center gap-2">
                    <i class="fa-brands fa-github"></i> View GitHub Repository
                </a>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-16">

        <!-- Section 1: Early Warning Radar -->
        <section id="radar" class="scroll-mt-20">
            <div class="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
                <div>
                    <h2 class="text-2xl font-bold text-white flex items-center gap-2">
                        <i class="fa-solid fa-radar text-emerald-400"></i> Early Warning Radar
                    </h2>
                    <p class="text-slate-400 text-sm mt-1">Real-time legislative and judicial developments across monitored global vectors.</p>
                </div>
                <div class="flex gap-2">
                    <input type="text" id="searchInput" placeholder="Search bills, keywords, states..." onkeyup="filterResults()" class="bg-slate-900 border border-slate-800 rounded-lg px-4 py-2 text-sm text-slate-200 focus:outline-none focus:border-emerald-500 w-64">
                </div>
            </div>

            <!-- Findings Grid/Table -->
            <div class="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-sm text-slate-300">
                        <thead class="bg-slate-950 text-slate-400 uppercase text-xs font-semibold border-b border-slate-800">
                            <tr>
                                <th class="px-6 py-4">Source / Jurisdiction</th>
                                <th class="px-6 py-4">Identifier / Case</th>
                                <th class="px-6 py-4">Title / Scope</th>
                                <th class="px-6 py-4">Trigger Keyword</th>
                                <th class="px-6 py-4 text-right">Action</th>
                            </tr>
                        </thead>
                        <tbody id="findingsTable" class="divide-y divide-slate-800">
                            <!-- Populated via JavaScript -->
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- Section 2: Automated Threat Feeds -->
        <section id="feeds" class="scroll-mt-20 border-t border-slate-800 pt-12">
            <h2 class="text-2xl font-bold text-white flex items-center gap-2 mb-2">
                <i class="fa-solid fa-rss text-emerald-400"></i> Automated Threat Feeds
            </h2>
            <p class="text-slate-400 text-sm mb-6">Programmatic access to raw policy intelligence output files for security research and automated pipelines.</p>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="bg-slate-900 border border-slate-800 p-6 rounded-xl">
                    <div class="text-emerald-400 text-xl font-bold mb-2">Structured JSON Feed</div>
                    <p class="text-slate-400 text-xs mb-4">Complete raw scan payload with jurisdiction metadata, primary URLs, and threat vector tags.</p>
                    <a href="https://github.com/wh1sper1/open-policy-engine/tree/main/pipeline/scrapers/output" target="_blank" class="text-emerald-400 hover:underline text-sm font-semibold flex items-center gap-1">
                        Access Scraper Outputs <i class="fa-solid fa-arrow-right text-xs"></i>
                    </a>
                </div>
                <div class="bg-slate-900 border border-slate-800 p-6 rounded-xl">
                    <div class="text-emerald-400 text-xl font-bold mb-2">Open States Vector</div>
                    <p class="text-slate-400 text-xs mb-4">Direct active monitoring feed targeting 3D printing, telemetry, and cryptography laws across all 50 US states.</p>
                    <a href="https://openstates.org" target="_blank" class="text-emerald-400 hover:underline text-sm font-semibold flex items-center gap-1">
                        OpenStates API Metadata <i class="fa-solid fa-arrow-right text-xs"></i>
                    </a>
                </div>
                <div class="bg-slate-900 border border-slate-800 p-6 rounded-xl">
                    <div class="text-emerald-400 text-xl font-bold mb-2">Judicial Precedent Feed</div>
                    <p class="text-slate-400 text-xs mb-4">CourtListener API v3 legal opinion index tracking federal DMCA 1201 and CFAA court rulings.</p>
                    <a href="https://www.courtlistener.com" target="_blank" class="text-emerald-400 hover:underline text-sm font-semibold flex items-center gap-1">
                        CourtListener Docket Search <i class="fa-solid fa-arrow-right text-xs"></i>
                    </a>
                </div>
            </div>
        </section>

        <!-- Section 3: Verified Policy Dossiers -->
        <section id="dossiers" class="scroll-mt-20 border-t border-slate-800 pt-12">
            <h2 class="text-2xl font-bold text-white flex items-center gap-2 mb-2">
                <i class="fa-solid fa-file-contract text-emerald-400"></i> Verified Policy Dossiers
            </h2>
            <p class="text-slate-400 text-sm mb-6">CI-validated, peer-reviewed legal and technical briefs backing legislative defense.</p>
            
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                <div>
                    <span class="inline-block px-2.5 py-0.5 rounded text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 mb-2">[VERIFIED]</span>
                    <h3 class="text-lg font-bold text-white">01: Flipper Zero Import Bans & Dual-Use Restrictions</h3>
                    <p class="text-slate-400 text-sm mt-1">Analysis of FCC/CBP import seizures, radio-frequency spectrum compliance, and hardware restrictions.</p>
                </div>
                <a href="https://github.com/wh1sper1/open-policy-engine/tree/main/dossiers" target="_blank" class="bg-slate-800 hover:bg-slate-700 text-slate-200 px-4 py-2 rounded-lg text-sm font-medium transition whitespace-nowrap">
                    Read Whitepaper
                </a>
            </div>
        </section>

        <!-- Section 4: Crowdsourced Hub -->
        <section id="submit" class="scroll-mt-20 border-t border-slate-800 pt-12">
            <div class="bg-gradient-to-r from-emerald-950/40 to-slate-900 border border-emerald-500/30 rounded-2xl p-8 text-center md:text-left md:flex items-center justify-between gap-8">
                <div>
                    <h2 class="text-2xl font-bold text-white mb-2">Submit Policy Intelligence</h2>
                    <p class="text-slate-400 text-sm max-w-2xl">Spotted a new state bill restricting 3D printers? Found a vendor changing driver-signing policies or remote disablement terms? Submit a report directly into our CI pipeline.</p>
                </div>
                <div class="mt-6 md:mt-0 flex flex-col sm:flex-row gap-3">
                    <a href="https://github.com/wh1sper1/open-policy-engine/issues/new?template=01_bill_submission.md" target="_blank" class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold px-4 py-2.5 rounded-lg text-sm transition">
                        Report Bill
                    </a>
                    <a href="https://github.com/wh1sper1/open-policy-engine/issues/new?template=02_vendor_policy_change.md" target="_blank" class="border border-slate-700 bg-slate-900 hover:bg-slate-800 text-slate-200 font-semibold px-4 py-2.5 rounded-lg text-sm transition">
                        Report Vendor Policy
                    </a>
                </div>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-800 bg-slate-950 py-8 text-center text-xs text-slate-500">
        <p>Open Policy Engine — Open Source Evidence-Driven Policy Intelligence.</p>
    </footer>

    <!-- Interactive Script -->
    <script>
        const findings = {findings_json};

        function renderTable(data) {{
            const tbody = document.getElementById('findingsTable');
            tbody.innerHTML = '';

            if (data.length === 0) {{
                tbody.innerHTML = `<tr><td colspan="5" class="px-6 py-8 text-center text-slate-500">No findings logged yet. Run the global scraper pipeline to populate live data.</td></tr>`;
                return;
            }}

            data.forEach(item => {{
                const row = document.createElement('tr');
                row.className = "hover:bg-slate-800/50 transition";
                row.innerHTML = `
                    <td class="px-6 py-4 font-semibold text-emerald-400">${{item.source || 'Unknown'}} (${{item.jurisdiction || 'N/A'}})</td>
                    <td class="px-6 py-4 font-mono text-xs text-slate-300">${{item.bill_id || 'N/A'}}</td>
                    <td class="px-6 py-4 text-slate-200">${{item.title || 'Untitled'}}</td>
                    <td class="px-6 py-4"><span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-xs border border-slate-700">${{item.keyword || 'General'}}</span></td>
                    <td class="px-6 py-4 text-right">
                        ${{item.url ? `<a href="${{item.url}}" target="_blank" class="text-emerald-400 hover:underline font-semibold text-xs">View Source <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i></a>` : '<span class="text-slate-600">No Link</span>'}}
                    </td>
                `;
                tbody.appendChild(row);
            }});
        }}

        function filterResults() {{
            const query = document.getElementById('searchInput').value.toLowerCase();
            const filtered = findings.filter(f => 
                (f.title && f.title.toLowerCase().includes(query)) ||
                (f.jurisdiction && f.jurisdiction.toLowerCase().includes(query)) ||
                (f.keyword && f.keyword.toLowerCase().includes(query)) ||
                (f.bill_id && f.bill_id.toLowerCase().includes(query))
            );
            renderTable(filtered);
        }}

        // Initial render
        renderTable(findings);
    </script>
</body>
</html>
"""

docs_file = docs_dir / "index.html"
docs_file.write_text(html_content, encoding="utf-8")
print(f"✅ Website generated successfully at: {docs_file}")