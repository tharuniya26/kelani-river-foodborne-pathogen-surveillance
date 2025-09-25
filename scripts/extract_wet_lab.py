"""Extract only embedded photographs in the original report, without altering pixels."""
import csv
from pathlib import Path
import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Research Project Report 12th Nov 2025.pdf"
OUT = ROOT / "assets/wet_lab"
SELECTED_FOR_README = {2, 4, 6, 13, 19, 27, 29, 35}
# The report's figure-list order matches the embedded image order on these pages.
CAPTIONS = {
    14: [
        (1, "Mannitol salt agar before incubation"), (2, "Mannitol salt agar after incubation"),
        (3, "Salmonella-Shigella agar before incubation, presumptive Salmonella workflow"),
        (4, "Salmonella-Shigella agar after incubation, presumptive Salmonella workflow"),
        (5, "Salmonella-Shigella agar before incubation, presumptive Shigella workflow"),
        (6, "Salmonella-Shigella agar after incubation, presumptive Shigella workflow"),
        (7, "Nutrient agar slants before incubation"),
    ],
    17: [(12, "Gram stain preparation for suspected Staphylococcus"),
         (13, "Microscopy of suspected Staphylococcus"),
         (14, "Smear from suspected Staphylococcus colonies"),
         (15, "Catalase test after hydrogen peroxide addition"),
         (16, "Urease broth before incubation for suspected Staphylococcus"),
         (17, "Urease broth after incubation for suspected Staphylococcus"),
         (18, "Mannitol salt agar before incubation"),
         (19, "Mannitol salt agar after incubation")],
    18: [(20, "Gram stain smear from suspected Salmonella"),
         (21, "Microscopy of suspected Salmonella"),
         (22, "Tryptone broth before incubation for suspected Salmonella"),
         (23, "Indole test after Kovac reagent for suspected Salmonella"),
         (24, "Urea broth before incubation for suspected Salmonella"),
         (25, "Urea broth after incubation for suspected Salmonella"),
         (26, "Kligler iron agar before inoculation for suspected Salmonella"),
         (27, "Kligler iron agar after incubation for suspected Salmonella")],
    19: [(28, "Gram stain smear from suspected Shigella"),
         (29, "Microscopy of suspected Shigella"),
         (30, "Tryptone broth before incubation for suspected Shigella"),
         (31, "Indole test after Kovac reagent for suspected Shigella"),
         (32, "Urea broth before incubation for suspected Shigella"),
         (33, "Urea broth after incubation for suspected Shigella"),
         (34, "Kligler iron agar before inoculation for suspected Shigella"),
         (35, "Kligler iron agar after incubation for suspected Shigella")],
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(SOURCE)
    records = []
    for page_number, figures in CAPTIONS.items():
        images = [x for x in doc[page_number - 1].get_images(full=True) if x[1] == 0]
        placements = [(x, doc[page_number - 1].get_image_rects(x[0])[0]) for x in images]
        placements.sort(key=lambda item: item[1].y0)
        rows = []
        for item in placements:
            if not rows or item[1].y0 - rows[-1][0][1].y0 > 15:
                rows.append([])
            rows[-1].append(item)
        images = [item[0] for row_items in rows for item in sorted(row_items, key=lambda item: item[1].x0)]
        if len(images) != len(figures):
            raise RuntimeError(f"Page {page_number}: found {len(images)} images for {len(figures)} figures")
        for (figure, caption), image in zip(figures, images):
            extracted = doc.extract_image(image[0])
            ext = extracted["ext"]
            filename = f"report_p{page_number:02d}_fig{figure:02d}.{ext}"
            (OUT / filename).write_bytes(extracted["image"])
            rights = ("Pending rights review; tracked in local Git for README preview"
                      if figure in SELECTED_FOR_README else "Pending rights review; local file excluded from Git")
            records.append([filename, SOURCE.name, page_number, figure, caption,
                            "Original university project report; attribution: Tharuniya Anpalakan and study team",
                            rights, extracted["width"], extracted["height"]])
    with (OUT / "image_inventory.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "source_pdf", "pdf_page", "figure_number", "source_caption_summary",
                         "attribution", "redistribution_status", "width_px", "height_px"])
        writer.writerows(records)
    print(f"Extracted {len(records)} original embedded images")


if __name__ == "__main__":
    main()
