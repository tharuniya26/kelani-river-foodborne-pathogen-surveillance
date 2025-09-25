"""Create and execute five standalone notebooks against the same src modules."""
from pathlib import Path
import nbformat as nbf
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks"

SPECS = [
    ("01_data_extraction_and_validation", "Validate the transcribed source readings",
     "The dataset contains abstract, matching report-result, and one conflicting report-discussion reading. Only authenticated aggregates are represented.",
     "from src.data_processing import load_data, published_data\nfrom src.statistical_analysis import gut_denominator_sensitivity\nall_rows = load_data()\npublished = published_data(all_rows)\nprint('Source rows:', len(all_rows), 'Published rows:', len(published))\nprint('Staphylococcus gut sensitivity:', gut_denominator_sensitivity())"),
    ("02_exploratory_analysis", "Describe site-specific detection",
     "Percentages are positive specimens out of the reported denominator; they are not bacterial concentration or unique-fish totals across organisms.",
     "from src.descriptive_analysis import ranked_sites, percentage_point_range\nprint(ranked_sites()[['pathogen','anatomical_site','positive_count','total_count','detection_percentage']].to_string(index=False))\nprint('\\nWithin-group site range (percentage points):')\nprint(percentage_point_range().round(2).to_string())"),
    ("03_statistical_analysis", "Calculate marginal Wilson intervals",
     "Two-sided 95% Wilson score limits assume independent fish for a single marginal. Sites on each fish are repeated, so these are not paired contrast intervals or reproduced published p-values.",
     "from src.statistical_analysis import interval_table, wilson_interval\nci = interval_table()\nprint(ci[['pathogen','anatomical_site','detection_percentage','wilson_low','wilson_high']].round(3).to_string(index=False))\nprint('27/27 Wilson bounds:', wilson_interval(27, 27))"),
    ("04_visualization", "Rebuild the scientific figures",
     "The figures derive only from the published abstract's 12 aggregate counts. The workflow is a reconstruction and original laboratory photographs are separate source evidence.",
     "from src.visualization import generate_figures\nfrom pathlib import Path\ngenerate_figures()\nprint('Generated PNGs:', [p.name for p in sorted(Path('figures').glob('*.png'))])"),
    ("05_results_and_interpretation", "Interpret the evidence and limitations",
     "The published abstract reports p < 0.001, p = 0.17 and p = 0.041 for the three groups, but specimen linkage and the original test are unavailable. No new confirmatory p-value is computed. The report's 22/25 reading and Shigella percentage errors remain documented.",
     "from src.descriptive_analysis import percentage_point_range\nfrom src.statistical_analysis import gut_denominator_sensitivity\nprint('Site ranges (percentage points):')\nprint(percentage_point_range().round(2).to_string())\nprint('Gut denominator alternatives:', {n: round(100*p,2) for n,p in gut_denominator_sensitivity().items()})\nprint('Paired site inference: not identifiable from aggregate margins')"),
]


def main():
    OUT.mkdir(exist_ok=True)
    for stem, title, explanation, code in SPECS:
        notebook = nbf.v4.new_notebook(cells=[
            nbf.v4.new_markdown_cell(f"# {title}\n\n{explanation}\n\nInput: `data/processed/organ_detection_summary.csv`. The source is the supplied conference abstract, with report comparison in the same table. See `docs/statistical_limitations.md` and `docs/source_reconciliation.md`."),
            nbf.v4.new_code_cell(code),
            nbf.v4.new_markdown_cell("## Interpretation and assumptions\n\nOutputs are derived from reported aggregate counts. They do not identify individual fish, confirm bacterial species, estimate bacterial load, or establish a cause of human disease. The original p-values remain reported but unverified."),
        ])
        notebook.metadata.kernelspec = {"display_name": "Python 3", "language": "python", "name": "python3"}
        NotebookClient(notebook, timeout=120, kernel_name="python3", resources={"metadata": {"path": str(ROOT)}}).execute()
        nbf.write(notebook, OUT / f"{stem}.ipynb")
        print(f"Executed {stem}")


if __name__ == "__main__":
    main()
