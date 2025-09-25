# Project audit — 16 October 2026

## Verified deliverables

- Original proposal (15 pages), report (33 pages), and conference abstract (one page) inspected; originals left in the workspace root. The report contains a private student number on its cover and a scanned submission identifier in an appendix. Neither identifier was copied into public-facing derivatives.
- Exact published aggregate integers (12 organism-site cells) were transcribed into `scripts/build_data.py`; a second set of report-results rows and the conflicting report-discussion row retain provenance. The published table, generated figures, report and notebook results use only the 12 abstract rows.
- All 31 embedded laboratory images corresponding to report figures 1–7 and 12–35 were extracted and visually matched to original report pages 14 and 17–19. Original labels/pixels were preserved. No collection or anatomical sampling photographs were found. Eight selected images are tracked in local Git for the README gallery; the other 23 remain ignored. Redistribution permission is still pending.
- Six scientific figures have PNG and SVG versions. Five notebooks execute with saved outputs and no error cells. Three validation tests pass. The new report PDF was rendered and inspected after generation.
- The original publication's five authors and printed affiliation superscripts, the University of Sri Jayewardenepura connection, principal supervisor Senior Professor Pathamalal M. Manage, and Mr Anjana Kelum acknowledgement remain credited.

## Independent results and limits

The software recalculates all 12 detection percentages from the reported integers, the within-organism ranges, 95% marginal Wilson intervals, and a literal 22/25 versus 22/27 sensitivity. It does **not** reproduce the abstract's p-values (<0.001, 0.17, 0.041). The original test, linked fish-by-organism outcomes and complete sampling metadata are absent. No species, virulence, infection incidence or contamination source was confirmed by this computational work.

## Source discrepancies and verification still needed

1. Report discussion p20 prints `22/25 (81.48%)`; report results p15 and abstract p189 report `22/27 (81.48%)`. A literal 22/25 is 88.00%.
2. Report discussion p21 pairs Shigella gill and gut counts with each other's percentages. Report results p16 and abstract p189 agree on 11/27 gills and 5/27 gut.
3. Report methods p13 names fish taxa that differ from the four taxa listed in the abstract; authentic specimen-level records are needed to reconcile species composition and sample inclusion.
4. The abstract page shows PP–137 and p189 but does not verify the conference edition, date/year, proceedings title, publisher, DOI or review status. A complete citation must await authoritative bibliographic evidence.
5. The PDFs do not document which named researcher personally performed each specific wet-lab step. Tharuniya's documented project-report authorship is clear; further personal technique claims require confirmation or lab records.
6. Source-PDF and embedded-photo redistribution rights require the author/institution or publisher's decision. The eight gallery images are tracked for private review, so their links resolve in a clone. They must not be released publicly until rights are confirmed. The three original PDFs remain excluded and unchanged.

## Privacy and rights gate for public release

The original PDFs are excluded from Git. Confirm rights for the five-author abstract, university proposal/report and source photographs separately; if photo rights are denied, remove the eight tracked gallery files and their README embeds before publication. Review the proposal/report cover pages and appendix for personal identifiers before any public upload; do not alter archival originals. The MIT license covers repository Python source code only. The derived aggregate table, new figures and reanalysis report should be reviewed by the original study team before external publication. AI assistance in code and editorial preparation is disclosed in README and report.

## Original-file integrity

| PDF | SHA-256 |
|---|---|
| Proposal | `9b6f5abd2696a5bf917a8e223aa3512add1d9eed7190011628f03d6b7eda700f` |
| Final report | `1053487a7abe4c9083770a48ba7a9f6bb96b1a497fab10a50bb05a4a4e5db9a9` |
| Conference abstract | `7273c2920c5932ad5aa20cf64e09c6ce0a02ee5e84fb2ff1c0ca004cd2be446a` |

## Readiness

The computational materials are locally reproducible. Public GitHub publication remains conditional on image/PDF rights review, private-identifier review, confirmation of the conference citation and personal wet-lab contribution claims. A private repository may be used for review; it must not be made public until those checks are complete. Git commit dates reflect actual repository work, while original study dates are documented in [research timeline](research_timeline.md).
