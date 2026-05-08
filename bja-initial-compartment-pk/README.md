# RAPM Narrative Review: Route-Aware Pharmacokinetic Modelling in Regional Anesthesia

## Are Intravenous Pharmacokinetic Models Fit for Purpose in Regional Anesthesia? The Case for Route-Aware Simulation of Local Anesthetic Absorption

静脈内投与由来の薬物動態モデルは区域麻酔に適用可能か？ — 局所麻酔薬の吸収に関する投与経路対応型シミュレーションの必要性

## Target Journal

**Regional Anesthesia & Pain Medicine (RAPM)** — Narrative Review

## Preprint

SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6614761

## Contents

### Manuscripts (Editable .docx)
- `RAPM_Manuscript_English.docx` — English manuscript (RAPM Narrative Review format, ~4200 words)
- `RAPM_Manuscript_Japanese.docx` — Japanese manuscript (parallel structure)

### Cover Letter
- `RAPM_Cover_Letter_English.docx` — Cover letter emphasizing monitoring window insight

### Figures (High-resolution PNG/TIFF, 300 dpi)
- `figures/figure1_compartment_models.png/.tiff` — IV model vs depot-augmented model comparison
- `figures/figure2_pk_simulation.png/.tiff` — Simulated plasma concentration–time profiles by route
- `figures/figure3_workflow.png/.tiff` — PBPK model development and validation workflow

### Build Scripts (Python)
- `generate_figures.py` — Generates Figures 1–3
- `build_en.py` — Builds English .docx manuscript
- `build_jp.py` — Builds Japanese .docx manuscript
- `build_cover_letter_en.py` — Builds English cover letter

### Legacy (BJA submission, archived)
- `BJA_Manuscript_English.docx` / `BJA_Manuscript_Japanese.docx`
- `BJA_Cover_Letter_English.docx` / `BJA_Cover_Letter_Japanese.docx`
- `BJA_Figures_English.pptx` / `BJA_Figures_Japanese.pptx`
- `generate_figure4.py` (removed from RAPM version)

## Key Message

Route-dependent absorption of local anesthetics after regional blocks has **two inseparable clinical consequences**:

1. **Dose safety** — Slow tissue absorption explains why doses exceeding traditional limits can be tolerated for fascial plane/peripheral nerve blocks (Cmax is lower than IV models predict)
2. **Monitoring duration** — The same delayed absorption shifts Tmax later, requiring extended observation periods to capture the true window of maximum LAST risk

## Build Instructions

```bash
pip install python-docx matplotlib numpy
python generate_figures.py
python build_en.py
python build_jp.py
python build_cover_letter_en.py
```

## Key References
- De Cassai A, et al. *BJA* 2025 — Epinephrine and fascial plane block pharmacokinetics
- Onishi T. SSRN Preprint 2025 — Initial compartment-dependent PK modelling
- PK-Sim / MoBi: https://www.open-systems-pharmacology.org/
