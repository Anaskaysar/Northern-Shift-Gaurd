# Northern Shift Guard — Paper

LaTeX source for the arXiv preprint and mining industry conference submissions.

## Build

Requires a TeX distribution (MacTeX, TeX Live).

```bash
cd paper
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Or with `latexmk`:

```bash
latexmk -pdf main.tex
```

Output: `main.pdf`

## Structure

```
paper/
├── main.tex                 # Master document
├── references.bib           # Bibliography
├── sections/                # One file per section
├── figures/                 # Publication-quality figures (300 DPI)
└── submissions/             # Venue-specific abstracts & cover letters
    └── sme_minexchange_2027_abstract.txt
```

## Submissions

| Venue | What | Deadline | File |
|-------|------|----------|------|
| **SME MINEXCHANGE 2027** | Abstract (100 words) | **Aug 1, 2026** | `submissions/sme_minexchange_2027_abstract.txt` |
| **SME MINEXCHANGE 2027** | Acceptance notification | Oct 31, 2026 | — |
| **SME MINEXCHANGE 2027** | Final manuscript (optional) | Nov 15, 2026 | `main.tex` |
| **SME MINEXCHANGE 2027** | Presentation (mandatory if accepted) | Feb 28 – Mar 3, 2027 | Denver |
| **arXiv** | Preprint PDF | Rolling | `main.tex` → compile → upload PDF |
| **CIM Convention** | TBD (~Feb–Mar annually) | Adapt from `main.tex` |
| **OneMine** | Rolling | Adapt from `main.tex` |

## Figures needed

| Figure | Status | Source |
|--------|--------|--------|
| Architecture diagram | ✅ Ready | `../docs/system_architecture.svg` → export PDF |
| Dashboard UI | ✅ Ready | `../submission_media/07_app_dashboard.jpg` |
| Scan results | ✅ Ready | `../submission_media/05_demo_scan_results.jpg` |
| Zone-flip comparison | ❌ TODO | Generate from eval pipeline |
| Baseline comparison chart | ❌ TODO | Generate from `eval/run_eval.py` |
| Audit trail | ✅ Ready | `../submission_media/08_audit_trail.jpg` |

## Writing status

- [x] Abstract skeleton
- [x] Section stubs
- [x] Starter bibliography
- [ ] Evaluation results (blocked on `eval/`)
- [ ] Full introduction draft
- [ ] Related work complete
- [ ] Method section complete
- [ ] Results section complete
- [ ] SME abstract finalized
- [ ] arXiv submission
