# LaTeX reanalysis manuscript

[Read the typeset PDF](../computational_reanalysis_latex.pdf) or edit [the LaTeX source](computational_reanalysis.tex). The manuscript preserves the original five-author publication credit, university affiliations and supervisor acknowledgements, and distinguishes the later computational extension.

It includes the full 12-row detection and Wilson interval table, the interval equation, six computational figures, denominator sensitivity, selected original laboratory photographs, interpretation, references and reproducibility instructions. Original photographs are included for private review, subject to the repository's redistribution conditions.

## Build

Install the root `requirements.txt` dependencies and a TeX distribution (MiKTeX or TeX Live) with `pdflatex` on PATH. Packages used: `fontenc`, `mathptmx`, `geometry`, `graphicx`, `xcolor`, `booktabs`, `amsmath`, `fancyhdr`, `caption`, and `hyperref`.

From the repository root:

```powershell
python -m scripts.build_latex_report
```

The builder calculates `generated/detection_intervals.tex` and `generated/denominator_sensitivity.tex` from the shared analysis modules, exports `data/processed/published_detection_intervals.csv`, refreshes the six computational figures and runs `pdflatex` twice. Compilation uses a temporary directory. The final PDF is copied into `reports/` only after compilation succeeds without overflowing boxes, missing characters or unresolved references. Tables marked generated should be changed through the source data or analysis code.

For a manual build using the existing generated tables and figure assets, run `pdflatex computational_reanalysis.tex` twice from this directory. Auxiliary build files are ignored by Git.
