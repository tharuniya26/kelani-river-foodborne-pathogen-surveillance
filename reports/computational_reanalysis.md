# Computational reanalysis and visualization of previously reported microbiological findings

**Prepared by:** Tharuniya Anpalakan, 16 October 2026. Computational extension of a University of Sri Jayewardenepura research project; not a second experimental publication.

**Original conference authors:** Anpalakan T; Meddage AKMMK; Liyanage GY; Idroos FS; Manage PM. The supplied abstract is printed as PP–137 on page 189. The author identifies it with the 12th International Conference on Multidisciplinary Approaches (iCMA 2026), Faculty of Graduate Studies, University of Sri Jayewardenepura. Exact proceedings metadata and peer-review status remain unverified; see publications/README.md for the evidence. The university report names Senior Professor Pathamalal M. Manage as principal supervisor and thanks Mr Anjana Kelum.

## Abstract

Published aggregate culture-based detections from 27 fish were transcribed and cross-checked against the university project report. Twelve organism-by-anatomical-site proportions were recalculated, visualized and accompanied by descriptive 95% Wilson score intervals. The largest site range was observed for presumptive *Staphylococcus* (44.4 percentage points). The report discussion contains a 22/25 versus 22/27 denominator conflict and swapped Shigella percentages. The original paired analysis cannot be reconstructed without linked specimen outcomes and a specified test. The study's detection patterns are descriptive evidence of presumptive organisms at sampled sites; they do not establish species-level identity, contamination source, or human disease risk.

## 1. Background and objectives

Fish skin, mouth and gills contact the surrounding water and handling environment, while gut material reflects ingestion and residence. The original study used these sites to compare presumptive bacterial detection. This extension aims to preserve the original counts, reconcile source discrepancies, quantify marginal uncertainty, and document the limits of aggregate inference. Relevant context is in `docs/research_background.md`.

## 2. Original experimental methods and provenance

The report documents fish collection through local fishermen, swabs and tissue samples, saline suspensions, dilution, enrichment, mannitol salt agar, Salmonella-Shigella agar, Gram staining, microscopy and biochemical tests. Original culture and test photographs occur on report pages 14 and 17–19. Individual performance of each bench technique is not attributable from the PDFs. The conference abstract is the primary source for the 12 detection counts; report results pages 15–16 corroborate them. The supplied documents do not contain linked specimen records.

## 3. Computational methods

`scripts/build_data.py` transcribes source-attributed integers and calculates percentages. `src/data_processing.py` validates values and source labels. `src/statistical_analysis.py` calculates two-sided 95% Wilson intervals for each marginal proportion. `src/visualization.py` produces the figures. No independent-sample significance test is applied to repeated anatomical sites. The original p-values are reported without claim of reproduction.

## 4. Results

| Reported group | Skin | Mouth | Gills | Gut |
|---|---:|---:|---:|---:|
| Staphylococcus spp. | 27/27 | 27/27 | 15/27 | 22/27 |
| Salmonella spp. | 11/27 | 9/27 | 10/27 | 4/27 |
| Shigella spp. | 9/27 | 15/27 | 11/27 | 5/27 |

Recalculated proportions span 55.6–100.0% for Staphylococcus, 14.8–40.7% for Salmonella and 18.5–55.6% for Shigella. These describe detection frequency, not bacterial concentration. The report discussion's alternative Staphylococcus gut denominator gives 22/25 = 88.0%, compared with 22/27 = 81.5% in both report results and abstract. The difference is 6.52 percentage points. The report discussion mispairs Shigella gill and gut counts with percentages; its results and the abstract agree on the counts.

## 5. Interpretation

The findings support site-specific detection patterns in this sampled material. Presumptive genus labels and limited biochemical tests cannot independently prove species, virulence or toxin production. The within-fish site observations are paired; no linked binary outcomes or full original test method were supplied, so Cochran's Q, McNemar and the published p-values cannot be independently reconstructed. Wilson intervals are marginal descriptions conditional on fish-level sampling assumptions. Handling and wastewater management are reasonable public-health topics, but this dataset does not estimate consumer infection risk or prove a contamination route.

## 6. Limitations and conclusions

The study has 27 fish, uncertain sampling frame, no released linked records, conflicting report wording, and no independent molecular or serological confirmation in the supplied report. New figures and code improve transparency, but they cannot repair missing original observations. The repository is suitable as a reproducible computational extension when clearly labelled. The original PDFs and photographs require privacy and redistribution clearance before GitHub publication.

## References and reproducibility

1. Supplied conference abstract: Anpalakan T; Meddage AKMMK; Liyanage GY; Idroos FS; Manage PM. 12th International Conference on Multidisciplinary Approaches (iCMA 2026); 2026. PP–137, p189. Conference association confirmed by the author. http://graduate.sjp.ac.lk/icma/icma-2026
2. Supplied university report: Tharuniya Anpalakan, project report, cover submission date 15 November 2025.
3. Mahagamage MGYL, Pathirage MVSC, Manage PM. Contamination Status of Salmonella spp., Shigella spp. and Campylobacter spp. in Surface and Groundwater of the Kelani River Basin, Sri Lanka. *Water*. 2020;12:2187. https://www.mdpi.com/2073-4441/12/8/2187
4. FDA. Bacteriological Analytical Manual, Chapter 5: Salmonella. https://www.fda.gov/food/laboratory-methods-food/bam-chapter-5-salmonella
5. CDC. About Staph Food Poisoning. https://www.cdc.gov/staph-food-poisoning/about/

Run the commands in `docs/reproducibility.md`. This report is generated from this editable Markdown source and figures by `scripts/build_report.py`. AI assistance supported code and editorial drafting; source attribution and scientific limitations are explicit.
