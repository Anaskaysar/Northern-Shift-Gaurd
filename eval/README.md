# Evaluation pipeline

Reproducible metrics for the Northern Shift Guard research paper.

## Quick start

```bash
cd eval
python run_eval.py
```

Output: `results/report.json`

## What it measures

| Metric | Baseline | Description |
|--------|----------|-------------|
| **False alarm rate** | B1 global vs B4 zone-aware | Non-compliant verdict when ground truth is compliant (surface zone) |
| **Zone-flip accuracy** | B4 | Same image: surface pass + active stope fail |
| **PPE precision/recall** | Ground-truth labels | Per-class hard hat and hi-vis (expand with live vision calls) |

## Baselines

| ID | Module | Description |
|----|--------|-------------|
| B1 | `baselines/global_rules.py` | Hard hat + hi-vis always required |
| B4 | `baselines/zone_aware.py` | Full zone compliance engine |

B2 (vision-only) and B3 (YOLO + global) to be added.

## Dataset

Labels in `dataset/labels.json`. Each entry:

```json
{
  "image_id": "fail_missing_hardhat",
  "hard_hat": "fail",
  "hi_vis": "fail",
  "ground_truth_compliance": {
    "surface": "non_compliant",
    "active_stope": "non_compliant"
  },
  "zone_flip_case": true
}
```

### Expand the dataset

1. Download [jhboyo/ppe-dataset](https://huggingface.co/datasets/jhboyo/ppe-dataset) or SH17
2. Add entries to `labels.json` with manual labels
3. Set `zone_flip_case: true` for images missing hard hat but hi-vis pass
4. Re-run `python run_eval.py`

Target: **150+ images** for arXiv, **300+** for SME full paper.

## Results for paper

After running eval, copy metrics into `paper/sections/results.tex`:

- `false_alarm_reduction_pct` → headline result
- `zone_flip_accuracy` → zone-flip experiment
- `hard_hat.f1`, `hi_vis.f1` → PPE detection table

## Next steps

- [ ] Add live GPT-4o vision eval (replace ground-truth-as-prediction)
- [ ] Add YOLO baseline (B3)
- [ ] Generate zone-flip figure from results
- [ ] Add reasoning quality rubric scoring script
- [ ] Export LaTeX tables to `results/tables/`
