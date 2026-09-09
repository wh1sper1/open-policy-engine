from pathlib import Path
import subprocess

templates = {
    ".github/ISSUE_TEMPLATE/01_bill_submission.md": """---
name: "Legislative Bill Report"
about: "Report a state or federal bill impacting encryption, maker rights, dual-use tools, or driver autonomy."
title: "[BILL]: <Jurisdiction> - <Bill Number> (<Brief Title>)"
labels: ["type: bill-submission", "needs-triaging"]
assignees: ""
---

## Bill Overview
- **Jurisdiction:** (e.g., California, Colorado, US Federal, EU)
- **Bill Number & Title:** (e.g., CO SB24-123 - Additive Manufacturing Regulations)
- **Current Legislative Status:** (e.g., Introduced, In Committee, Passed, Signed)
- **Primary Source Link:** (Must link directly to official legislature domain, e.g., `.gov` or Open States)

## Vector Category
- [ ] Cryptography & Security Restrictions
- [ ] Maker Controls (3D Printing / CNC / Serialization)
- [ ] Digital Ecosystem Lock-in
- [ ] Automotive Autonomy & Driver Agency

## Key Statutory Snippet
> *Paste exact quotes from the introduced or amended bill text targeting technology, software, or hardware specifications.*

## Taxonomy Classification
- [ ] **[VERIFIED]** Enacted law or official bill draft on government record.
- [ ] **[PLAUSIBLE]** Proposed committee amendment or ALEC model bill.
- [ ] **[ALLEGED]** Speculative claim regarding sponsor motive (Requires attached written statement/manifesto).

## Impact Analysis
*Briefly explain how this bill restricts open-source tools, hardware modification, or user agency.*
""",
    ".github/ISSUE_TEMPLATE/02_vendor_policy_change.md": """---
name: "Vendor Policy / TOS Change"
about: "Report a vendor policy, driver-signing enforcement, OS lock-in, or tool classification change."
title: "[VENDOR]: <Company/Platform> - <Policy Name or Action>"
labels: ["type: vendor-policy", "needs-triaging"]
assignees: ""
---

## Vendor & Target System
- **Company / Platform:** (e.g., Microsoft, Apple, Tesla, npm, Google)
- **Product / Subsystem:** (e.g., Windows Defender, Secure Boot, OEM Firmware, App Store Policies)
- **Official Policy URL:** (Must link to vendor documentation, advisory, or official TOS)

## Policy Action Type
- [ ] Driver Signing / Secure Boot Barrier
- [ ] Security Tool Flagged as Malware (e.g., Flipper Zero, pen-testing tools)
- [ ] Package Registry / License Constraint
- [ ] Firmware / Right-to-Repair Lockout
- [ ] Telemetry / Mandatory Cloud Requirement

## Evidence Artifact
- **Document / Commit / Release Date:**
- **Exact Policy Wording or Advisory ID:**
- **Archived Source / Diff Link:**

## Taxonomy Classification
- [ ] **[VERIFIED]** Confirmed via official vendor documentation, security advisory, or code repository.
- [ ] **[ALLEGED]** Unconfirmed report or behavior observed in beta/unreleased software.
""",
    ".github/ISSUE_TEMPLATE/03_court_precedent.md": """---
name: "Court Ruling / Legal Precedent"
about: "Report a federal or state court decision regarding CFAA, DMCA 1201, encryption, or privacy."
title: "[COURT]: <Case Name> (<Court Name> / <Year>)"
labels: ["type: court-precedent", "needs-triaging"]
assignees: ""
---

## Case Information
- **Full Case Name:** (e.g., *State v. Doe* or *EFF v. Department of Justice*)
- **Court & Docket Number:** (e.g., 9th Circuit Court of Appeals, No. 22-15000)
- **Date of Order / Ruling:**
- **Official Docket Link:** (Must link to court record, CourtListener, or official opinion PDF)

## Statutory Area
- [ ] Compelled Decryption / 5th Amendment
- [ ] DMCA Section 1201 Exemptions
- [ ] Computer Fraud and Abuse Act (CFAA)
- [ ] Administrative Procedure Act (APA) / Agency Overreach
- [ ] Platform Antitrust & Hardware Bundling

## Core Holding Summary
> *Paste or summarize the exact legal holding established in the written opinion.*

## Taxonomy Classification
- [ ] **[VERIFIED]** Binding ruling, signed consent order, or published appellate opinion.
- [ ] **[PLAUSIBLE]** Active complaint, pending motion, or interlocutory order.
"""
}

def main():
    for path_str, content in templates.items():
        p = Path(path_str)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        print(f"✅ Created: {path_str}")

    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "feat: add GitHub issue templates for bills, vendor policies, and court rulings"], check=True)
    print("\n🎉 Templates committed to Git successfully!")

if __name__ == "__main__":
    main()