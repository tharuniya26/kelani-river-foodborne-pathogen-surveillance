# Data provenance

The three untouched PDFs in the workspace root are the original evidence. The supplied conference abstract, printed p189, is the primary source for all 12 counts; the university report results pp15–16 independently repeat them. Counts were manually read and transcribed into `scripts/build_data.py`; proportions and percentages are calculated from integers by that script. `src/data_processing.py` validates the derived table. No specimen-level rows, fish-species assignments, coordinates, colony counts or disease outcomes were inferred.

The alternative 22/25 is preserved as a separate row, with its own source page and verification status. Original photographs in `assets/wet_lab/` are embedded image bytes extracted from report pp14 and 17–19. Eight selected photographs are tracked in the local Git repository for README review; the other 23 remain excluded. Redistribution rights for all photographs remain pending, and nothing has been pushed publicly. The images do not establish which named researcher performed each photographed procedure.

The original PDF SHA-256 values can be regenerated with `Get-FileHash -Algorithm SHA256 *.pdf` on PowerShell or `sha256sum *.pdf` on Unix. Never overwrite a source PDF during this workflow. Computational figures and the new PDF report are newly derived works.
