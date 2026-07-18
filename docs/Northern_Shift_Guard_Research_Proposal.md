# Northern Shift Guard: Research Proposal

## From Visual Evidence to Grounded Action: A Zone-Aware Vision-Language Framework with Retrieval-Augmented Reasoning and Auditable Decision Chains

**Status:** Active — Dataset construction phase (M1)
**Last updated:** July 18, 2026

---

## Author Team

| Role | Person | Contribution |
|---|---|---|
| **Lead Author** | Kaysarul Anas Apurba | Architecture, backend, evaluation design, paper writing |
| **Co-Author** | Kazeem Oguntade | Dataset construction, domain framing, annotation |
| **Co-Author (TBD)** | Laurentian University contact | Human annotation, ground truth verification, manuscript review |
| **Domain Validator (Vacancy)** | Mining/industrial safety professional | Zone-flip case validation, Ontario Reg 854 compliance review, 20–30 case expert annotation |

### Domain Validator — Open Position

**What we need:** One person with background in Northern Ontario mining operations, industrial safety, or Ontario Reg 854 compliance who can:
- Review 20–30 zone-flip cases and confirm whether system verdicts are clinically/operationally correct
- Validate zone PPE requirements against real mine-site practice
- Provide a quote or acknowledgment for the paper's evaluation section

**What they get:** Co-author credit (if contribution is substantive) or named acknowledgment. No technical work required — domain judgment only.

**How to onboard:** Share the zone-flip case set (JSON + images) and a simple rubric. 2–3 hours total commitment.

---

## Research Goal

Publish a citable arXiv preprint and workshop paper demonstrating expertise in:
- Multimodal LLM reasoning pipelines
- Retrieval-Augmented Generation (RAG) over regulatory text
- Explainable and auditable AI for high-stakes decisions
- Context-aware decision logic (zone rules as structured knowledge)

**Mining is the testbed. The contribution is the decision chain architecture.**

The same architecture applies to healthcare triage, legal compliance, industrial inspection, and any regulated domain requiring zone-specific, auditable AI decisions.

---

## The Publishable Claim

> A three-layer decision architecture (vision evidence → zone compliance → LLM reasoning) produces zone-specific supervisor actions with a full audit trail — and the same visual evidence yields different compliance outcomes depending on mine zone context, reducing false alarms compared to global-rule baselines.

This "same photo, different zone, different verdict" result is concrete, testable, and directly publishable. Generic PPE detectors do not address this.

---

## Contributions

| # | Contribution | Description |
|---|---|---|
| **C1** | Three-layer decision architecture | Separates perception (what was seen), compliance (what the zone requires), and reasoning (what to do and why) |
| **C2** | Zone-context compliance engine | Config-driven PPE requirements per mine zone, grounded in Ontario Reg 854 |
| **C3** | Auditable AI design | Every scan stores vision JSON, compliance breakdown, Nemotron action, and timestamp |
| **C4** | Zone-flip empirical result | Same image under different zones produces different compliance verdicts — reducing false alarms vs global-rule baselines |
| **C5** | Human-validated evaluation | Expert domain validator confirms zone-flip verdicts against real mine-site practice (20–30 cases) |
| **C6** | Deployable reference system | End-to-end FastAPI + React pipeline with Docker deployment |

---

## Research Questions

- **RQ1:** Does zone-aware compliance logic reduce false alarms compared to global-rule PPE detection baselines, and by how much?
- **RQ2:** Does incorporating agent reasoning traces (Nemotron) over retrieved regulatory context improve supervisor action quality compared to vision-only or rule-only approaches?
- **RQ3:** How does the system perform across mine zones with different PPE requirements (surface yard vs active stope vs open pit)?
- **RQ4:** What is the latency and cost tradeoff of the full three-layer pipeline versus simpler baselines?

---

## System Architecture

```
Worker Photo + Zone Selection
         │
         ▼
┌─────────────────────────────┐
│   Stage 1: Vision Evidence  │  GPT-4o vision → structured JSON
│   (PPE detection + fatigue) │  {hard_hat, hi_vis, fatigue_risk}
└─────────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Stage 2: Zone Compliance   │  Config-driven rules per zone
│  (Ontario Reg 854)          │  Required vs detected vs compliant
└─────────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Stage 3: LLM Reasoning     │  Nemotron + safety refs RAG
│  (Grounded action)          │  Prioritized supervisor action
└─────────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Audit Log (SQLite)         │  Zone, evidence JSON, compliance,
│                             │  action, timestamp — full trail
└─────────────────────────────┘
```

**Key differentiator:** The product is the decision chain, not the bounding box.

---

## Milestone Plan

| # | Milestone | Owner | Status | Target |
|---|---|---|---|---|
| **M1** | Dataset construction (150+ images) | Kazeem + Kaysarul | 🔄 Active | Week 1–2 |
| **M2** | Baselines + quantitative metrics | Kaysarul | ⏸ Blocked on M1 | Week 2–3 |
| **M3** | Zone-flip experiment + figures | Kaysarul | ⏸ Blocked on M2 | Week 3–4 |
| **M4** | Domain validator onboarded | Kaysarul (recruit) | 🔍 Recruiting | Week 2 |
| **M5** | Expert annotation (20–30 cases) | Domain validator | ⏸ Blocked on M4 | Week 3–4 |
| **M6** | Human inter-rater annotation | LU contact (TBD) | ⏸ Blocked on M1 | Week 3–4 |
| **M7** | Paper draft (LaTeX) | Kaysarul | ⏸ Blocked on M3 | Week 4–5 |
| **M8** | arXiv preprint | All | ⏸ Blocked on M7 | Week 5–6 |
| **M9** | Workshop submission | All | ⏸ Blocked on M8 | Week 6–8 |

**Fast path target:** arXiv live by September 2026 — before PhD application deadlines.

---

## Evaluation Plan

### Dataset Construction (M1) — Kazeem leads

**Target:** 150+ images minimum for arXiv; 300+ for workshop submission.

| Source | Size | Owner | Purpose |
|---|---|---|---|
| Public PPE datasets (SH17, jhboyo) | 100–150 | Kazeem | Baseline PPE accuracy |
| Curated mining/industrial photos | 30–50 | Kazeem | Domain-relevant scenarios |
| Existing demo set | ~10 | Kaysarul | Seed cases, zone-flip examples |
| Synthetic zone assignments | All | Both | Label each image with applicable zones |

**Label schema per image:**

```json
{
  "image_id": "img_001",
  "hard_hat": "pass | fail | unclear",
  "hi_vis": "pass | fail | unclear",
  "fatigue_risk": "low | medium | high | unclear",
  "applicable_zones": ["surface", "open_pit", "active_stope"],
  "ground_truth_compliance": {
    "surface": "compliant | non_compliant",
    "active_stope": "compliant | non_compliant"
  },
  "annotator_1": "kaysarul",
  "annotator_2": "kazeem",
  "domain_validator": "TBD",
  "inter_rater_agreement": null,
  "source": "sh17 | construction_ppe | curated | demo"
}
```

**Human annotation protocol:**
- Kaysarul and Kazeem independently label all images
- Compute inter-rater agreement (Cohen's Kappa) on PPE labels
- Domain validator independently reviews 20–30 zone-flip cases
- Disagreements resolved by discussion; final label recorded with note

This directly addresses the reviewer gap from SciRet — human verification is built into the dataset construction, not added as an afterthought.

### Baselines (M2)

| Baseline | Description | Expected weakness |
|---|---|---|
| **B1: Global rules** | Hard hat + hi-vis always required regardless of zone | False alarms on surface zone where hard hat not required |
| **B2: Vision-only (GPT-4o)** | Visual detection, no zone context, pass/fail only | No zone-specific guidance, no audit |
| **B3: YOLO + global rules** | YOLOv8 PPE detector + global compliance | No reasoning, no zone context, no audit trail |
| **B4: Full pipeline (Northern Shift Guard)** | Vision + zone compliance + Nemotron reasoning | Target system |

### Metrics (M3)

| Metric | Definition | Baseline comparison |
|---|---|---|
| **PPE detection accuracy** | Precision/recall for hard_hat and hi_vis vs ground truth | B2, B3 vs B4 |
| **Zone-flip accuracy** | Correct compliance verdict when zone changes for same image | B1 vs B4 — headline result |
| **False alarm reduction** | (B1 false alarms − B4 false alarms) / B1 false alarms | Quantifies C4 |
| **Reasoning quality score** | Expert rubric 1–5 on action correctness, grounding, clarity | B2, B3 vs B4 |
| **Inter-rater agreement** | Cohen's Kappa on PPE labels between Kaysarul and Kazeem | Data quality signal |
| **Domain validator agreement** | Expert vs system verdict on 20–30 zone-flip cases | C5 — human validation |
| **End-to-end latency** | Upload → full response (p50, p95) | Deployment feasibility |
| **Cost per scan** | GPT-4o + Nemotron API cost per analysis | Practical deployment |

### Zone-Flip Experiment — Headline Result (M3)

**Protocol:**
1. Select 20–30 images where hard hat is **absent** but worker is otherwise compliant
2. Run each image through pipeline with zone = **Surface / Yard**
3. Run same image with zone = **Active Stope**
4. Record compliance verdict, supervisor action, and reasoning output for each
5. Domain validator reviews all 20–30 cases and confirms verdict correctness

**Expected result:**

| Zone | Hard hat required? | System verdict | Validator confirms? |
|---|---|---|---|
| Surface / Yard | No | ✅ Compliant — no action | TBD |
| Active Stope | Yes | ❌ Non-compliant — stop-work | TBD |

**Headline metric:** False alarm rate of B1 (global rules) vs B4 (zone-aware) on this subset, validated by domain expert.

### Human Annotation Protocol — Addressing SciRet Gap

Three-layer human verification built into evaluation design:

**Layer 1 — Inter-annotator agreement (Kaysarul + Kazeem):**
- Both independently label all 150+ images for PPE presence
- Compute Cohen's Kappa — target κ > 0.7 (substantial agreement)
- Report in paper as data quality metric

**Layer 2 — Expert domain validation (Mining safety professional):**
- Receives 20–30 zone-flip cases as image + zone + system verdict
- Simple rubric: Is the compliance verdict correct for this zone? (Yes / No / Uncertain)
- Reports agreement rate with system
- Named in paper as domain validator

**Layer 3 — Reasoning quality rubric (3 reviewers):**
- Kaysarul, Kazeem, and one additional reviewer (LU contact TBD)
- Rate 25–30 Nemotron outputs on 4 criteria (1–5 scale):
  - Action correctness
  - Regulatory grounding
  - Explainability clarity
  - Practical usability
- Report mean ± std, inter-rater agreement

### Ablation Studies

| Ablation | Compare | Research question |
|---|---|---|
| Zone context | With vs without zone in Nemotron prompt | Does zone context improve action quality? |
| Safety references (RAG) | With vs without `data/safety_refs/` | Does regulatory retrieval improve grounding? |
| Reasoning model | Nemotron vs GPT-4o-mini fallback | Quality vs cost tradeoff |
| Vision model | GPT-4o vs YOLO | Accuracy vs latency tradeoff |

---

## Paper Structure

```
1. Introduction
   1.1 Motivation: shift-start safety gap in Northern Ontario mining
   1.2 Limitations of global PPE detection — the zone-blind problem
   1.3 Contributions C1–C6
   1.4 Paper organization

2. Related Work
   2.1 PPE detection in industrial and mining settings
   2.2 Vision-language models for safety violation detection (MonitorVLM)
   2.3 LLM reasoning in industrial safety contexts
   2.4 Explainable and auditable AI in regulated domains
   2.5 Positioning vs closest prior work

3. Problem Formulation
   3.1 Mine zones and PPE requirements (Ontario Reg 854)
   3.2 The zone-blind failure mode — formal definition
   3.3 Decision outputs: compliance verdict, supervisor action, audit record
   3.4 Human-in-the-loop constraints and scope

4. Method
   4.1 System overview (architecture diagram)
   4.2 Stage 1: Vision evidence extraction (GPT-4o structured JSON)
   4.3 Stage 2: Zone compliance engine (config-driven rules)
   4.4 Stage 3: Nemotron reasoning over evidence + RAG over safety refs
   4.5 Audit log schema and traceability design
   4.6 Deployment (FastAPI + React + Docker — brief)

5. Experimental Setup
   5.1 Dataset construction and annotation protocol
   5.2 Inter-annotator agreement methodology
   5.3 Domain validator protocol and credentials
   5.4 Baselines (B1–B4)
   5.5 Metrics
   5.6 Evaluation protocol

6. Results
   6.1 PPE detection performance (B1–B4 comparison)
   6.2 Zone-flip experiment — headline result
   6.3 False alarm reduction quantification
   6.4 Reasoning quality scores (rubric + inter-rater agreement)
   6.5 Domain validator agreement on zone-flip cases
   6.6 Ablation studies
   6.7 Latency and cost analysis

7. Discussion
   7.1 What the zone-flip result means for mining operations
   7.2 Comparison to MonitorVLM and related systems
   7.3 Generalizability to other regulated domains
   7.4 Fatigue screening scope and limitations
   7.5 Privacy, consent, and deployment ethics

8. Limitations and Future Work
   8.1 Dataset size and domain shift (construction vs mining)
   8.2 Cloud API dependency — offline fallback requirement
   8.3 No real mine-site deployment yet
   8.4 Limited PPE types (hard hat + hi-vis only)
   8.5 Lighting conditions for underground environments

9. Conclusion

Appendix
   A. Zone configuration schema (zones.json)
   B. Prompt templates (vision + reasoning)
   C. Sample audit records
   D. Supervisor evaluation rubric
   E. Domain validator case set (20–30 images)
```

---

## Target Venues

### Primary — Do these

| Venue | Fit | Deadline | Travel |
|---|---|---|---|
| **arXiv (cs.AI + cs.IR)** | ✅ 5.0/5 | Rolling — target Sep 2026 | None |
| **ACL/EMNLP NLP-app workshop** | ✅ 4.0/5 | Check CFP — late 2026 | Often hybrid |
| **AAAI AISI workshop** | ✅ 4.0/5 | Check CFP — late 2026 | Often hybrid |
| **NeurIPS Safe ML workshop** | ✅ 3.5/5 | Check CFP — Aug/Sep 2026 | Often hybrid |

### Secondary — If evaluation is strong

| Venue | Fit | What's needed |
|---|---|---|
| **FAccT** | 3.0/5 | Accountability framing, ethics section |
| **AIES** | 3.0/5 | Human-in-the-loop analysis expanded |
| **EMNLP Findings** | 2.5/5 | Stronger RAG ablations, larger dataset |

### Skip

- CHI — requires supervisor UX/trust user study
- CVPR/ICCV main — wrong contribution framing
- SME MINEXCHANGE — US visa blocker

---

## PhD Application Value

| Application piece | What this paper demonstrates |
|---|---|
| **SOP** | Multimodal LLM reasoning, RAG over regulatory text, XAI in high-stakes domains |
| **CV** | arXiv preprint + workshop paper (if accepted) |
| **Professor emails** | "I have a preprint on zone-aware VLM reasoning with RAG and auditable decision chains" |
| **Skills demonstrated** | GPT-4o vision, structured LLM output, RAG, rule-based + neural hybrid, evaluation design, human annotation protocol |

**Target professors this paper supports:**
- Dehghantanha (Guelph) — XAI + AI security application
- Kathleen Fraser (uOttawa) — AI safety + regulated domains
- Zhijing Jin (UofT) — adversarial robustness + responsible AI
- Hila Gonen (UBC) — LLM safety + reliable AI systems

---

## Limitations to State Explicitly

| Limitation | How to frame it |
|---|---|
| Fatigue screening is visual aid only | Not medical diagnosis; supervisor is decision-maker |
| Small evaluation set | Prototype-origin; production requires mine-site dataset |
| Cloud API dependency | GPT-4o + Nemotron MVP; offline fallback is future work |
| No real mine-site deployment | Validated on public + curated images; field trial is future work |
| Limited PPE types | Hard hat + hi-vis only; gloves, boots, respirators are roadmap |
| Domain shift | Public datasets are construction/manufacturing; mining transfer is approximate |
| Lighting conditions | Vision degrades underground; checkpoint lighting required for production |
| Privacy and consent | Production requires retention policy, union agreements, role-based access |

---

## Open Questions — Resolve Before Paper Draft

- [ ] Who is the LU contact for annotation (Layer 3 reviewer)? Confirm before M6.
- [ ] Domain validator — who, how to approach, timeline for onboarding?
- [ ] Will Kazeem be available for the full evaluation phase or just dataset construction?
- [ ] Paper template — COLM style for arXiv preprint, switch to ACL for workshop submission?
- [ ] Do we need IRB/ethics approval for using public PPE images? Check SH17 license.

---

## References (Starter BibTeX)

```bibtex
@article{monitorvlm2025,
  title={MonitorVLM: A Vision Language Framework for Safety
         Violation Detection in Mining Operations},
  journal={arXiv preprint arXiv:2510.03666},
  year={2025}
}

@article{mdse2026,
  title={From 3D Perception to Safety Reasoning: A Graph-Based
         Framework for Real-Time Underground Mine Monitoring},
  journal={arXiv preprint arXiv:2606.03460},
  year={2026}
}

@misc{ontario854,
  title={Ontario Regulation 854: Mines and Mining Plants},
  author={{Government of Ontario}},
  year={1990},
  note={R.R.O. 1990, Reg. 854}
}

@dataset{sh17,
  title={SH17 Dataset for PPE Detection},
  author={Mughees, Ahmad and others},
  year={2023},
  url={https://github.com/ahmadmughees/SH17dataset}
}

@dataset{jhboyo_ppe,
  title={PPE Dataset},
  author={jhboyo},
  year={2023},
  url={https://huggingface.co/datasets/jhboyo/ppe-dataset}
}
```

---

## Notes

- SciRet EMNLP decision: July 30, 2026 — does not affect Northern Shift Guard timeline
- If SciRet accepted: Northern Shift Guard + SciAgentIR run in parallel
- If SciRet rejected: Northern Shift Guard continues; SciRet revision pauses SciAgentIR
- Kazeem is confirmed as co-author — coordinate on dataset construction this week
- Domain validator slot is open — priority to fill before M3 (zone-flip experiment)
