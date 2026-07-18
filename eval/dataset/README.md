# Milestone 1 — Dataset Construction

**Status:** 🔄 In progress  
**Owner:** You  
**Do not proceed to Milestone 2 until this checklist is complete.**

Everything else (baselines, paper results, arXiv, SME) waits on this.

---

## Goal

Build a labeled evaluation set in `eval/dataset/` that supports:

1. PPE detection accuracy (hard hat, hi-vis)
2. Zone-flip experiment (same image → different zone → different verdict)
3. Fatigue screening cases (optional but useful)
4. False-alarm analysis (global rules vs zone-aware)

### Target sizes

| Tier | Images | Enough for |
|------|--------|------------|
| **Minimum** | 50 | Internal validation, proof of eval pipeline |
| **arXiv** | 150 | Preprint with credible numbers |
| **SME / industry conference** | 300+ | Full paper submission |

### Current count

| Source | Count | Target |
|--------|-------|--------|
| Demo (`sample_images/`) | 3 labeled | 10 |
| Zone-flip cases | 1 (placeholder, no image yet) | 20–30 |
| Public PPE datasets | 0 | 100–200 |
| Curated mining/industrial | 0 | 30–50 |
| **Total** | **4 entries** | **150+** |

---

## Folder layout

```
eval/dataset/
├── README.md              ← this file
├── labels.json            ← master label file (one entry per image)
├── images/                ← copy or symlink eval images here
│   ├── demo/              ← from sample_images/
│   ├── sh17/              ← from SH17 dataset
│   ├── construction_ppe/  ← from Ultralytics dataset
│   ├── jhboyo/            ← from Hugging Face dataset
│   └── curated/           ← manually collected mining/industrial photos
└── schema.json            ← optional: JSON schema for validation
```

**Convention:** Every image referenced in `labels.json` should live under `eval/dataset/images/<source>/`.

---

## Label schema

Each entry in `labels.json` → `images[]`:

```json
{
  "image_id": "unique_snake_case_id",
  "filename": "original_filename.jpg",
  "path": "images/sh17/img_0042.jpg",
  "hard_hat": "pass",
  "hi_vis": "fail",
  "fatigue_risk": "low",
  "applicable_zones": ["surface", "open_pit", "active_stope"],
  "ground_truth_compliance": {
    "surface": "non_compliant",
    "active_stope": "non_compliant"
  },
  "zone_flip_case": false,
  "source": "sh17",
  "split": "eval",
  "notes": "Optional: labeling rationale or edge case notes"
}
```

### Field rules

| Field | Values | Rule |
|-------|--------|------|
| `hard_hat` | `pass` / `fail` / `unclear` | `pass` = clearly visible on head |
| `hi_vis` | `pass` / `fail` / `unclear` | `pass` = hi-vis vest/jacket on torso |
| `fatigue_risk` | `low` / `medium` / `high` / `unclear` | Visible cues only — not medical |
| `zone_flip_case` | `true` / `false` | `true` only when surface ≠ active_stope compliance |
| `source` | `demo` / `sh17` / `construction_ppe` / `jhboyo` / `curated` | Track provenance |
| `split` | `eval` | Hold out from any future training |

### Auto-deriving `ground_truth_compliance`

Use zone rules from `backend/config/zones.json`:

| Zone | Required PPE |
|------|-------------|
| `surface` | hi-vis only |
| `open_pit` | hard hat + hi-vis |
| `underground_entry` | hard hat + hi-vis |
| `active_stope` | hard hat + hi-vis |
| `processing_plant` | hard hat + hi-vis |

**Compliance logic per zone:**
- Required item + `pass` → compliant for that item
- Required item + `fail` or `unclear` → non-compliant for that zone
- Not required → does not affect compliance

You can label `hard_hat` / `hi_vis` manually, then compute compliance — or label compliance directly and cross-check.

---

## Image categories to collect

Aim for balanced coverage:

| Category | Target count | `hard_hat` | `hi_vis` | `zone_flip_case` |
|----------|-------------|------------|----------|------------------|
| Fully compliant | 30–50 | pass | pass | false |
| Missing hard hat only | 20–30 | fail | pass | **true** |
| Missing hi-vis only | 20–30 | pass | fail | false |
| Missing both | 20–30 | fail | fail | false |
| Unclear / partial occlusion | 10–20 | unclear | pass/fail | false |
| Fatigue cues visible | 10–15 | any | any | false |
| **Zone-flip headline cases** | **20–30** | fail | pass | **true** |

The **zone-flip headline case** is the most important for the paper:
- Worker has hi-vis but no hard hat
- Surface / Yard → **compliant**
- Active Stope → **non-compliant**

Current placeholder: `zone_flip_no_hardhat` in `labels.json` — **needs a real image**.

---

## Data sources

### 1. Demo set (already in repo)

Copy from `sample_images/` → `eval/dataset/images/demo/`

| File | Labels | Zone-flip? |
|------|--------|------------|
| `pass_compliant.jpg` | hat=pass, vest=pass | No |
| `fail_missing_hardhat.jpg` | hat=fail, vest=fail | No (both fail) |
| `fatigue_tired_operator.jpg` | hat=fail, vest=fail, fatigue=medium | No |

Also label the unlabeled files in `sample_images/`:
- `mining-workers-day.jpg`
- `images.jpg`, `images_1.jpg`, `images_2.jpg`, `images_3.jpg`

### 2. Public PPE datasets (primary bulk)

| Dataset | Link | Size | How to use |
|---------|------|------|------------|
| **SH17** | https://github.com/ahmadmughees/SH17dataset | 8,099 images | Has helmet, vest, head classes — best for mining transfer story |
| **Construction-PPE** | https://docs.ultralytics.com/datasets/detect/construction-ppe/ | Real construction scenes | helmet/no_helmet, vest/no_vest labels |
| **jhboyo/ppe-dataset** | https://huggingface.co/datasets/jhboyo/ppe-dataset | 15,500 images | Fast to download; YOLO format |

**Suggested workflow for public datasets:**

1. Download dataset
2. Sample 50–100 images stratified by class (helmet yes/no, vest yes/no)
3. Copy sampled images to `eval/dataset/images/<source>/`
4. Convert bbox labels → `hard_hat` / `hi_vis` pass/fail (or manually verify a subset)
5. Add entries to `labels.json`
6. Flag `zone_flip_case: true` for all hat=fail, vest=pass images

### 3. Curated mining/industrial (optional but strengthens paper)

- Pexels / Unsplash industrial worker photos (free license)
- OneMine / public mining safety photos
- Your own collected photos

Save to `eval/dataset/images/curated/` and label manually.

---

## Labeling workflow

### Step-by-step

```
1. Pick source          → demo / sh17 / construction_ppe / jhboyo / curated
2. Copy image           → eval/dataset/images/<source>/<filename>
3. Open image           → inspect hard hat, hi-vis, fatigue cues
4. Label PPE fields     → hard_hat, hi_vis, fatigue_risk
5. Compute compliance   → per zone using rules above
6. Set zone_flip_case   → true if surface=compliant AND active_stope=non_compliant
7. Add entry            → append to labels.json images[]
8. Validate             → python eval/dataset/validate.py (when ready)
```

### Labeling tips

- **Be conservative:** if unsure, use `unclear` — don't force pass/fail
- **One worker per image:** pick the primary subject if multiple people
- **Zone-flip cases are gold:** prioritize finding hat=fail + vest=pass images
- **Don't label from filename alone:** always open and verify the image
- **Track disagreements:** if two labelers disagree, note in `notes` field

### Quick reference — zone-flip check

```
hard_hat=fail + hi_vis=pass
  → surface:        compliant      ✓
  → active_stope:   non_compliant  ✓
  → zone_flip_case: true           ✓
```

---

## Milestone 1 checklist

Complete every item before moving to Milestone 2 (baselines & metrics).

### Setup
- [ ] Create `eval/dataset/images/` subfolders (`demo/`, `sh17/`, etc.)
- [ ] Copy and label all existing `sample_images/` files
- [ ] Add real image for `zone_flip_no_hardhat` placeholder

### Public datasets
- [ ] Download at least one public PPE dataset (SH17 or jhboyo recommended)
- [ ] Sample 50+ images with stratified PPE classes
- [ ] Label and add to `labels.json`

### Coverage
- [ ] ≥ 30 fully compliant images (both pass)
- [ ] ≥ 20 zone-flip cases (hat fail, vest pass)
- [ ] ≥ 20 missing hi-vis only (hat pass, vest fail)
- [ ] ≥ 20 missing both (hat fail, vest fail)
- [ ] ≥ 10 unclear/partial cases
- [ ] ≥ 10 fatigue cases (optional)

### Quality
- [ ] Every entry has valid `path` pointing to existing file
- [ ] Every entry has `ground_truth_compliance` for all applicable zones
- [ ] `zone_flip_case: true` entries verified manually
- [ ] Total count ≥ 50 (minimum) or ≥ 150 (arXiv target)

### Sign-off
- [ ] Run `python eval/run_eval.py` — no errors
- [ ] Review `eval/results/report.json` — numbers look reasonable
- [ ] Update count table at top of this README

---

## After Milestone 1

Only when the checklist above is complete:

| Milestone | What | Depends on |
|-----------|------|------------|
| **M2** | Baselines & metrics (B1–B4, full eval run) | M1 dataset |
| **M3** | Zone-flip experiment + figures | M2 results |
| **M4** | Paper results section | M3 figures |
| **M5** | arXiv preprint | M4 |
| **M6** | SME abstract submission | ⏸ Blocked on M1 (abstract only) | Due **Aug 1, 2026** |
| **M7** | SME presentation + optional manuscript | ⏸ After acceptance (**Oct 31, 2026**) | Manuscript **Nov 15** (optional) · present **Feb 2027** |

---

## Questions to decide before labeling

1. **Manual vs semi-automated labeling?**  
   Public datasets have bbox labels — you can auto-convert helmet present/absent, then manually verify a 10% sample.

2. **How many zone-flip cases?**  
   Minimum 20 for a credible paper claim. These are your headline result.

3. **Include fatigue labels on all images?**  
   Recommended: label `fatigue_risk` on all, but only 10–15 need `medium`/`high` for fatigue analysis.

4. **Hold out a test set?**  
   Use `split: "eval"` for all for now. If you fine-tune YOLO later, split train/eval then.

---

## Current seed entries

See `labels.json` — 4 entries:

| ID | Image | Status |
|----|-------|--------|
| `pass_compliant` | ✅ exists | Labeled |
| `fail_missing_hardhat` | ✅ exists | Labeled (not zone-flip) |
| `zone_flip_no_hardhat` | ❌ no image | **Needs real photo** |
| `fatigue_tired_operator` | ✅ exists | Labeled |

Start by fixing the zone-flip placeholder, then expand from public datasets.
