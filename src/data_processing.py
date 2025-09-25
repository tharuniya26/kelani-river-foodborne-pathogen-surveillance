"""Load and validate source-attributed aggregate detection counts."""
from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "data/processed/organ_detection_summary.csv"
REQUIRED = {"pathogen", "anatomical_site", "positive_count", "total_count",
            "detection_proportion", "detection_percentage", "source_document",
            "source_page", "source_table_or_section", "verification_status", "discrepancy_notes"}
PATHOGENS = {"Staphylococcus spp.", "Salmonella spp.", "Shigella spp."}
SITES = {"Skin", "Mouth", "Gills", "Gut"}


def load_data(path=DATA_PATH):
    return validate_data(pd.read_csv(path, keep_default_na=False))


def validate_data(frame):
    missing = REQUIRED - set(frame.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    if frame.empty or frame[list(REQUIRED - {"discrepancy_notes"})].isna().any().any():
        raise ValueError("Required fields must not be empty")
    for col in ("pathogen", "anatomical_site", "source_document", "source_page",
                "source_table_or_section", "verification_status"):
        if frame[col].astype(str).str.strip().eq("").any():
            raise ValueError(f"Blank {col}")
    if not set(frame.pathogen).issubset(PATHOGENS) or not set(frame.anatomical_site).issubset(SITES):
        raise ValueError("Unexpected organism or anatomical site")
    for col in ("positive_count", "total_count"):
        numeric = pd.to_numeric(frame[col], errors="raise")
        if numeric.isna().any() or (numeric % 1 != 0).any():
            raise ValueError(f"{col} must contain integers")
        frame[col] = numeric.astype(int)
    if ((frame.positive_count < 0) | (frame.total_count <= 0) |
            (frame.positive_count > frame.total_count)).any():
        raise ValueError("Invalid numerator or denominator")
    ratio = frame.positive_count / frame.total_count
    if not ((frame.detection_proportion.astype(float) - ratio).abs() < 1e-9).all():
        raise ValueError("Detection proportions disagree with counts")
    if not ((frame.detection_percentage.astype(float) - 100 * ratio).abs() < 1e-7).all():
        raise ValueError("Detection percentages disagree with counts")
    if frame.duplicated(["pathogen", "anatomical_site", "source_document", "source_page", "source_table_or_section"]).any():
        raise ValueError("Duplicate source observation")
    return frame


def published_data(frame=None):
    frame = load_data() if frame is None else validate_data(frame.copy())
    result = frame.loc[frame.verification_status == "published_abstract"].copy()
    if len(result) != 12 or result.duplicated(["pathogen", "anatomical_site"]).any():
        raise ValueError("Expected 12 unique published organ-by-organism rows")
    return result
