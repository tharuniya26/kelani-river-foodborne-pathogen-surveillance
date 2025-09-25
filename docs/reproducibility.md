# Reproducibility

Tested on Python 3.14.2, Windows, with versions pinned in `requirements.txt`. A fresh clone reproduces the derived table, figures and report from the committed aggregate transcription; the private source PDFs are needed only to independently audit extraction.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m scripts.build_data
python -m src.visualization
python -m pytest
python -m scripts.build_notebooks
python -m scripts.build_report
```

Run `python -m scripts.extract_wet_lab` only when the original report PDF is present locally. This extracts embedded images to a Git-ignored location. See `docs/source_reconciliation.md` before interpreting any aggregate contrast. `python -m scripts.build_notebooks` executes five notebooks and saves outputs using the same `src` functions.
