\# Verified Dossier 01: Flipper Zero Import Bans \& Dual-Use Restrictions



\*\*Taxonomy Status:\*\* `\[VERIFIED]`  

\*\*Primary Subjects:\*\* Wireless Protocols, FCC Spectrum Regulations, Import Restrictions, Dual-Use Tool Classification  

\*\*Target Entities:\*\* Innovation, Science and Economic Development Canada (ISED), US Customs and Border Protection (CBP)



\---



\## 1. Executive Summary



In early 2024, government entities—most notably Innovation, Science and Economic Development Canada (ISED)—announced initiatives aimed at prohibiting consumer penetration testing devices, explicitly citing the \*\*Flipper Zero\*\* under the justification of combatting automotive theft involving keyless entry systems. This dossier documents regulatory actions, legal standards, and primary technical evidence evaluating the classification of multi-tool wireless devices.



\---



\## 2. Regulatory Timeline \& Actions



\### A. Canadian Regulatory Initiatives (February 2024)

\* \*\*Agency Announcement:\*\* On February 8, 2024, Canadian Minister of Innovation, Science and Industry François-Philippe Champagne declared intent to ban the importation, sale, and use of consumer hacking devices used in auto thefts.

\* \*\*Scope:\*\* Targeted sub-GHz radio devices, specifically naming Flipper Zero, alleging participation in keyless signal replication.

\* \*\*Primary Source Citation:\*\* \[ISED Canada National Summit on Combatting Auto Theft](https://www.canada.ca/en/innovation-science-economic-development.html)



\### B. United States Customs Administration Holds

\* \*\*Customs Seizures:\*\* US Customs and Border Protection (CBP) previously subjected shipments of \~15,000 units to administrative holds at ports of entry under custom entry inquiries regarding RF compliance (FCC ID certification) and dual-use classification.

\* \*\*Legal Authority:\*\* 19 U.S.C. § 1499 (Customs Inspections and Holds) and FCC Title 47 CFR Part 15 regulations.



\---



\## 3. Technical Evidence \& Counter-Analysis



1\. \*\*Static vs. Rolling Codes:\*\* Modern vehicles (post-1995) rely on encrypted rolling code systems (e.g., KeeLoq, Hitag2). Flipper Zero factory firmware is constrained from transmitting on restricted sub-GHz frequencies or bypassing rolling code cryptosystems.

2\. \*\*Signal Repeaters vs. Sub-GHz Testing:\*\* Actual keyless auto theft relies primarily on high-power RF relay attack hardware (amplifying signals between key fobs inside a home and vehicles in driveways), an architecture distinct from low-power sub-GHz transceivers.

3\. \*\*Chilling Effect on Security Research:\*\* Classifying multi-use RF testing devices as contraband sets a precedent threatening general-purpose software-defined radios (SDRs), HackRF units, and educational STEM microcontrollers.



\---



\## 4. Primary Citations \& Evidence Log



\* \*\*\[Primary]\*\* Electronic Frontier Foundation Legal Analysis: \[Restricting Flipper is a Zero Accountability Approach](https://www.eff.org/deeplinks/2024/03/restricting-flipper-zero-accountability-approach-security-canadian-government)

\* \*\*\[Primary]\*\* Manufacturer Technical Statement: \[Flipper Devices Official Response to Canadian Authorities](https://blog.flipper.net/response-to-canadian-government/)

