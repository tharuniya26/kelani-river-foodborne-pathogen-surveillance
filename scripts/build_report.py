"""Render the editable Markdown research report as a PDF."""
import re
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "reports/computational_reanalysis.md"
OUTPUT = ROOT / "reports/computational_reanalysis.pdf"


def markup(text):
    text = escape(text).replace("–", "-").replace("’", "'")
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)
    text = re.sub(r"`(.*?)`", r"<font name='Courier'>\1</font>", text)
    return text


def build():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleCustom", parent=styles["Title"], fontSize=19, leading=24,
                              textColor=colors.HexColor("#123b52"), spaceAfter=20, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name="BodyCustom", parent=styles["BodyText"], fontSize=9.5, leading=14,
                              spaceAfter=8))
    styles.add(ParagraphStyle(name="HeadingCustom", parent=styles["Heading2"], fontSize=12,
                              textColor=colors.HexColor("#0072B2"), spaceBefore=13, spaceAfter=7))
    flow = []
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    paragraph = []

    def flush():
        if paragraph:
            flow.append(Paragraph(markup(" ".join(paragraph)), styles["BodyCustom"]))
            paragraph.clear()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            flush(); i += 1; continue
        if line.startswith("# "):
            flush(); flow.append(Paragraph(markup(line[2:]), styles["TitleCustom"])); i += 1; continue
        if line.startswith("## "):
            flush(); title = line[3:]
            flow.append(Paragraph(markup(title), styles["HeadingCustom"]))
            if title.startswith("4. Results"):
                pass
            i += 1; continue
        if line.startswith("|"):
            flush(); rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [cell.strip() for cell in lines[i].strip().strip("|").split("|")]
                if not all(set(cell) <= set("-: ") for cell in cells):
                    rows.append([Paragraph(markup(cell), styles["BodyCustom"]) for cell in cells])
                i += 1
            table = Table(rows, repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([("BACKGROUND", (0,0),(-1,0), colors.HexColor("#eaf4f6")),
                                       ("GRID",(0,0),(-1,-1),.3,colors.grey),
                                       ("VALIGN",(0,0),(-1,-1),"TOP"),
                                       ("LEFTPADDING",(0,0),(-1,-1),8),
                                       ("RIGHTPADDING",(0,0),(-1,-1),8)]))
            flow.append(KeepTogether([table, Spacer(1, 9)]))
            if rows and "Staphylococcus" in rows[1][0].text:
                for name, caption in [
                    ("01_heatmap", "Figure 1. Published detection percentages by organism and anatomical site."),
                    ("03_wilson_intervals", "Figure 2. Marginal 95% Wilson intervals; no paired contrast inferred."),
                    ("06_source_comparison", "Figure 3. Reconciliation of report and abstract readings.")]:
                    from reportlab.lib.utils import ImageReader
                    path = ROOT / "figures" / f"{name}.png"
                    iw, ih = ImageReader(str(path)).getSize()
                    width = min(6.8*inch, iw/2)
                    flow.extend([Image(str(path), width=width, height=width*ih/iw),
                                 Paragraph(caption, styles["BodyCustom"]), Spacer(1, 8)])
            continue
        if re.match(r"^\d+\. ", line):
            flush()
        paragraph.append(line)
        i += 1
    flush()

    def footer(canvas, doc):
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.grey)
        canvas.drawString(40, 28, "Computational reanalysis of previously reported findings")
        canvas.drawRightString(doc.pagesize[0]-40, 28, str(doc.page))

    SimpleDocTemplate(str(OUTPUT), pagesize=(595,842), leftMargin=46, rightMargin=46,
                      topMargin=42, bottomMargin=45, title="Computational reanalysis of Kelani River fish microbiology",
                      author="Tharuniya Anpalakan").build(flow, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    build()
