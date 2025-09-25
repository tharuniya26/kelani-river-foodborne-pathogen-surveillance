"""Transcribe and validate source-attributed aggregate counts from the supplied PDFs."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/processed/organ_detection_summary.csv"
COUNTS = {
    "Staphylococcus spp.": {"Skin": 27, "Mouth": 27, "Gills": 15, "Gut": 22},
    "Salmonella spp.": {"Skin": 11, "Mouth": 9, "Gills": 10, "Gut": 4},
    "Shigella spp.": {"Skin": 9, "Mouth": 15, "Gills": 11, "Gut": 5},
}
FIELDS = ["pathogen", "anatomical_site", "positive_count", "total_count",
          "detection_proportion", "detection_percentage", "source_document",
          "source_page", "source_table_or_section", "verification_status", "discrepancy_notes"]


def row(group, site, pos, total, document, page, section, status, note=""):
    return dict(zip(FIELDS, [group, site, pos, total, pos/total, 100*pos/total,
                             document, page, section, status, note]))


def build():
    rows = []
    abstract = "iCMA_FOOD BORNE PATHOGEN.pdf"
    report = "Research Project Report 12th Nov 2025.pdf"
    for group, sites in COUNTS.items():
        for site, pos in sites.items():
            note = "Report discussion p20 prints 22/25 but 81.48%." if group == "Staphylococcus spp." and site == "Gut" else ""
            if group == "Shigella spp." and site in {"Gills", "Gut"}:
                note = "Report discussion p21 swaps count-percentage pairings for gills and gut."
            rows.append(row(group, site, pos, 27, abstract, "PDF 1; printed 189", "Abstract", "published_abstract", note))
            page = 15 if group == "Staphylococcus spp." else 16
            rows.append(row(group, site, pos, 27, report, f"PDF {page}; printed {page}",
                            f"Results 5.1; Figure {9 + list(COUNTS).index(group)}", "report_results", note))
    rows.append(row("Staphylococcus spp.", "Gut", 22, 25, report, "PDF 20; printed 20",
                    "Discussion 6.0", "conflicting_report_text", "Printed 81.48% matches 22/27, not 22/25."))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(rows)


if __name__ == "__main__":
    build()
