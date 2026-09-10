# Verified Dossier 01: Import Bans & Dual-Use Restrictions on Single-Board Computers and Pen-Testing Hardware

**Taxonomy Status:** `[VERIFIED]`  
**Primary Subjects:** Single-Board Computers (SBCs), Sub-GHz Transceivers, Software-Defined Radio (SDR), FCC Regulations, Export Controls  
**Target Hardware:** Flipper Zero, HackRF One, Raspberry Pi / Orange Pi (SBCs), Wi-Fi Pineapple, BadUSB / Rubber Ducky  
**Regulatory Bodies:** Innovation, Science and Economic Development Canada (ISED), US Customs and Border Protection (CBP), US Department of Commerce (BIS)

---

## 1. Executive Summary

Regulatory agencies worldwide are increasingly targeting portable, general-purpose hardware capable of wireless analysis, keystroke injection, or signal capture under the umbrella of combatting crime and digital intrusion. 

This dossier analyzes regulatory holds, export control classifications (EAR/BIS), and import enforcement trends restricting dual-use hardware—including **Flipper Zero**, **HackRF One**, **Single-Board Computers (SBCs)**, and **Wi-Fi pen-testing tools**.

---

## 2. Targeted Hardware Classes & Dual-Use Profile

| Device Category | Representative Examples | Primary Dual-Use Function | Regulatory Friction / Risk Area |
| :--- | :--- | :--- | :--- |
| **Multi-Tool RF Analyzers** | Flipper Zero | Sub-GHz RF analysis, RFID/NFC testing, GPIO interfacing | Canadian ISED sales ban proposals; CBP port-of-entry holds |
| **Software-Defined Radios (SDR)** | HackRF One, BladeRF, LimeSDR | Wideband RF reception/transmission (1 MHz–6 GHz) | FCC Title 47 non-compliance holds; unshielded TX power limits |
| **Single-Board Computers (SBCs)** | Raspberry Pi, Orange Pi, Radxa | Low-cost computing, drop-boxes, automated penetration testing | ECCN 5A002 encryption controls; customs bulk import scrutinies |
| **Wi-Fi & Network Audit Tools** | Wi-Fi Pineapple, Alfa Wireless | Packet injection, rogue AP testing, captive portal research | FCC Part 15 signal compliance; export restrictions under BIS ACE exception |
| **Keystroke Injection Hardware** | USB Rubber Ducky, Bash Bunny | Human Interface Device (HID) emulation, administrative scripting | Vendor shipping restrictions and customs seizure flags |

---

## 3. Regulatory Frameworks & Enforcement Actions

### A. Canadian ISED Prohibitions on Hacking Tools (2024)
* **Agency Action:** Innovation, Science and Economic Development Canada (ISED) announced restrictions targeting consumer hacking tools under the rationale of preventing vehicle theft.
* **Overreach Vector:** While explicitly targeting sub-GHz tools like Flipper Zero, the regulatory wording risked encompassing general-purpose SDRs (HackRF One) and single-board computers configured for portable RF research.
* **Source Link:** [ISED Canada Policy Framework on Auto Theft Prevention](https://www.canada.ca/en/innovation-science-economic-development.html)

### B. US Customs and Border Protection (CBP) Holds
* **Administrative Enforcement:** CBP has subjected shipments of sub-GHz and SDR hardware to entry holds under **19 U.S.C. § 1499**, citing compliance audits under FCC Title 47 CFR Part 15 and uncertified RF transmission capabilities.
* **SBC & SDR Impact:** Importers of bulk single-board computers and SDR kits face increased compliance verification when devices lack fixed-frequency filtering.

### C. US Bureau of Industry and Security (BIS) Export Controls
* **Cybersecurity Controls:** BIS export regulations (Category 4 & 5 of the Commerce Control List) enforce strict licensing requirements on hardware and software designed for system intrusion or surveillance, impacting international distribution of specialized pen-testing hardware.

---

## 4. Primary Citations & Evidence Log

* **[Primary]** Electronic Frontier Foundation Legal Analysis: [Restricting Flipper & SDR Tools is a Zero-Accountability Approach](https://www.eff.org/deeplinks/2024/03/restricting-flipper-zero-accountability-approach-security-canadian-government)
* **[Primary]** US Department of Commerce BIS Rulemaking: [Cybersecurity Items Export Controls](https://www.bis.doc.gov/)
* **[Primary]** Manufacturer Technical Defense: [Flipper Devices Official Response to Regulatory Authorities](https://blog.flipper.net/response-to-canadian-government/)