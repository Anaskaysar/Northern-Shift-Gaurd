# Northern Shift Guard — Research Roadmap

Guide for extending the hackathon prototype into a **showcase research paper for PhD applications** in explainable AI, NLP, LLMs, and retrieval-augmented reasoning.

**Primary author:** Kaysarul Anas Apurba  
**Team:** NorthMind — Kaysarul Anas Apurba · Kazeem Oguntade  
**Status:** Hackathon complete (🥈 2nd Place Overall · 🧠 Best Use of Nemotron) → **Research extension active**  
**Last updated:** July 18, 2026

---

## Research goal (PhD application focus)

**Goal:** Publish a citable preprint/paper that showcases expertise in **explainable AI, NLP, LLM reasoning, and retrieval-augmented generation (RAG)** — using mining shift-start safety as the **application domain**, not the career target.

**What PhD committees should see:**
- Multi-stage VLM → structured evidence → LLM reasoning pipeline
- Context-aware decision logic (zone rules as structured knowledge)
- RAG over regulatory/safety text (`data/safety_refs/`)
- Auditable, human-in-the-loop AI design
- Rigorous evaluation (not just a demo)

**Mining is the testbed.** The contribution is the **decision chain architecture** — applicable to healthcare triage, legal compliance, industrial inspection, and other regulated domains.

### Constraints — SME MINEXCHANGE deprioritized

| Issue | Impact |
|-------|--------|
| Conference in **Denver, USA** (Feb 2027) | In-person attendance required if abstract accepted |
| **US visa barriers** (e.g. security deposit rules) | Cannot reliably attend → **mandatory presentation is a blocker** |
| Career goal is **PhD in XAI/NLP**, not mining industry | Industry conference has lower ROI than arXiv + ML/NLP workshops |

**Decision:** Do **not** pursue SME MINEXCHANGE unless visa situation changes. Focus on **arXiv + ML/NLP/XAI workshops** that accept remote or don't require US travel.

Archived SME materials remain in [`paper/submissions/`](../paper/submissions/) for reference only.

---

## Milestone tracker

Work proceeds **one milestone at a time**. Do not skip ahead.

| # | Milestone | Status | Guide |
|---|-----------|--------|-------|
| **M1** | **Dataset construction** | 🔄 **Active** | [`eval/dataset/README.md`](../eval/dataset/README.md) |
| M2 | Baselines & metrics | ⏸ Blocked on M1 | `eval/run_eval.py` |
| M3 | Zone-flip experiment + figures | ⏸ Blocked on M2 | `paper/figures/` |
| M4 | Paper results section | ⏸ Blocked on M3 | `paper/sections/results.tex` |
| M5 | **arXiv preprint** | ⏸ Blocked on M4 | `paper/main.tex` — **primary deliverable** |
| M6 | ML/NLP workshop submission | ⏸ Blocked on M5 | See [Target venues](#target-venues) |
| ~~M7~~ | ~~SME MINEXCHANGE~~ | ❌ **Deprioritized** | Visa/travel blocker; not aligned with PhD goals |

---

1. [Executive summary](#executive-summary)
2. [Why this is publishable](#why-this-is-publishable)
3. [Research contribution](#research-contribution)
4. [Related work & positioning](#related-work--positioning)
5. [What we have vs what we need](#what-we-have-vs-what-we-need)
6. [Paper framing](#paper-framing)
7. [Paper structure](#paper-structure)
8. [Evaluation plan](#evaluation-plan)
9. [Target venues](#target-venues)
10. [Timeline & milestones](#timeline--milestones)
11. [Repository assets for research](#repository-assets-for-research)
12. [Suggested folder layout](#suggested-folder-layout)
13. [Writing checklist](#writing-checklist)
14. [Limitations to state explicitly](#limitations-to-state-explicitly)
15. [Next actions](#next-actions)

---

## Executive summary

Northern Shift Guard is a strong candidate for both an **arXiv preprint** and a **mining industry conference paper**. The core idea — **zone-aware, explainable, auditable shift-start safety screening** — aligns with active 2026 research on vision-language models (VLMs) and LLM-driven decision intelligence in mining.

**The publishable claim is not:** “We detect hard hats.”

**The publishable claim is:**

> A three-layer decision architecture (vision evidence → zone compliance → reasoning) produces zone-specific supervisor actions with a full audit trail — and the same visual evidence can yield different compliance outcomes depending on mine zone context.

That “same photo, different zone, different verdict” result is a concrete, testable contribution that generic PPE detectors do not address.

| Target | Feasible? | Estimated effort |
|--------|-----------|------------------|
| **arXiv preprint** | ✅ Yes | 3–4 weeks with focused evaluation |
| **Mining industry conference (CIM, SME, OneMine)** | ✅ Very good fit | 4–8 weeks |
| **ML workshop paper** | ✅ Yes | 4–6 weeks |
| **Top-tier CS main track** | ⚠️ Hard without site partner + large benchmark | 2–3 months+ |

---

## Why this is publishable

### Timely research lane (2025–2026)

Industrial safety AI is moving beyond object detection toward **multimodal decision intelligence**:

- **MonitorVLM** — vision-language framework for mining safety violation detection from surveillance video ([arXiv:2510.03666](https://arxiv.org/abs/2510.03666))
- **MDSE / graph-based frameworks** — 3D perception + LLM safety reasoning for underground monitoring ([arXiv:2606.03460](https://arxiv.org/abs/2606.03460))
- **OneMine 2026 papers** — vision AI evolving from object detection to LLM-driven decision support in mining operations

Northern Shift Guard fits this trajectory but focuses on a distinct use case: **shift-start checkpoint screening** with **regulatory zone context** and **human-in-the-loop auditability** — not site-wide surveillance.

### Real-world problem alignment

Northern Ontario mines face:

- Workforce turnover and inexperienced workers at shift start
- Manual, inconsistent PPE and fatigue checks
- No documented record of what was seen or why a worker was cleared
- Zone-specific requirements under **Ontario Regulation 854** (surface yard ≠ active stope)

### Hackathon validation

- 🥈 **2nd Place Overall** — Cursor Hackathon Sudbury 2026
- 🧠 **Best Use of Nemotron** — NVIDIA Brev credits
- Track: **Mining & Industrial Innovation**

---

## Research contribution

Claim these as explicit contributions in the paper:

| # | Contribution | Description |
|---|--------------|-------------|
| **C1** | Three-layer decision architecture | Separates *perception* (what was seen), *compliance* (what the zone requires), and *reasoning* (what to do and why) |
| **C2** | Zone-context compliance engine | Config-driven PPE requirements per mine zone, grounded in Ontario Reg 854 |
| **C3** | Auditable AI design | Every scan stores vision JSON, compliance breakdown, Nemotron action, and timestamp |
| **C4** | Zone-flip empirical claim | Same image under different zones produces different compliance verdicts — reducing false alarms vs global-rule baselines |
| **C5** | Deployable reference system | End-to-end FastAPI + React pipeline with Docker deployment for shift-start workflows |

### Key differentiator (memorize this)

> **The product is the decision chain, not the bounding box.**

Detection → zone rules → prioritized supervisor action → audit record.

---

## Related work & positioning

### Comparison matrix

| Approach | What it does | Limitation | Our angle |
|----------|--------------|------------|-----------|
| **YOLO / object detection** | Detects helmet, vest, person | No zone context; no reasoning; global pass/fail | Add compliance + reasoning + audit layers |
| **MonitorVLM** | VLM safety violation detection from video | Surveillance-scale; clause filtering for regulations | Shift-start checkpoint; structured decision chain |
| **Graph-based underground monitoring** | 3D perception + LLM safety reasoning | Heavy infrastructure; underground focus | Lightweight shift-start workflow; zone config |
| **Generic safety LLM chatbots** | Natural-language safety Q&A | No structured vision evidence binding | Reasoning grounded in structured detections + zone context |
| **Site-wide CCTV analytics** | Continuous monitoring | Surveillance concerns; low supervisor trust | Scoped to human-in-the-loop checkpoint screening |

### Papers to cite

| Paper | Relevance |
|-------|-----------|
| MonitorVLM (2025) | Closest mining VLM safety work — cite and differentiate |
| MDSE / graph-based underground monitoring (2026) | LLM safety reasoning in mining |
| OneMine vision AI + LLM decision intelligence (2026) | Industry trend validation |
| SH17 / Construction-PPE datasets | PPE detection baselines |
| Ontario Reg 854 | Regulatory grounding |

### Search keywords for literature review

```
mining safety vision language model
PPE compliance computer vision
explainable AI industrial safety
zone-aware safety compliance
shift-start safety screening
auditable AI regulated industries
LLM reasoning safety violations
Northern Ontario mining safety
Ontario Regulation 854 PPE
```

---

## What we have vs what we need

### Already paper-ready ✅

| Asset | Location | Notes |
|-------|----------|-------|
| End-to-end architecture | `backend/`, `frontend/` | Vision → zone rules → Nemotron → SQLite audit |
| Zone compliance engine | `backend/zone_service.py`, `backend/config/zones.json` | 5 zones, per-item required/detected/compliant |
| Nemotron reasoning layer | `backend/nemotron_service.py` | NVIDIA NIM + OpenAI fallback + mock |
| Vision service | `backend/vision_service.py` | GPT-4o structured JSON output |
| Safety reference corpus | `data/safety_refs/` | Ontario Reg 854, OSHA, Northern context |
| Model notebook | `notebooks/northern_shift_guard.ipynb` | Prompt tuning, pipeline export |
| Architecture diagram | `docs/system_architecture.svg` | Figure-ready |
| Demo screenshots | `submission_media/` | Zone-flip, dashboard, audit trail |
| Project report | `docs/Northern_Shift_Guard_Project_Report.pdf` | Background material |
| Regulatory zone definitions | `backend/config/zones.json` | Surface, open pit, underground, stope, plant |

### Still needed for publication ❌

| Gap | Priority | Notes |
|-----|----------|-------|
| Formal evaluation dataset | **Critical** | Currently ~3 labeled demo cases; need 150–300+ images |
| Quantitative metrics | **Critical** | PPE accuracy, zone-flip accuracy, false alarm reduction |
| Baseline comparisons | **Critical** | Global rules, vision-only, YOLO-only, full pipeline |
| Ablation studies | **High** | w/ vs w/o zone context, Nemotron vs fallback, safety refs |
| Reasoning quality evaluation | **High** | Supervisor rubric or expert panel (3+ reviewers) |
| Latency / cost analysis | **Medium** | Per-scan API cost, end-to-end latency |
| LaTeX paper draft | **High** | Abstract, intro, method, experiments, conclusion |
| Mining site partner (optional) | **Medium** | Strengthens industry conference credibility |

---

## Paper framing

### Working title

> **Northern Shift Guard: A Zone-Aware Vision-Language Framework for Explainable and Auditable Mining Shift-Start Safety Screening**

### Alternative titles

- *From Detection to Decision: Zone-Context Compliance for Mining Shift-Start Safety*
- *Explainable Shift-Start Screening for Northern Ontario Mines: A Vision-Language Decision Framework*
- *Beyond PPE Detection: Zone-Aware Reasoning and Audit Trails for Mining Safety AI*

### Abstract skeleton (fill in after evaluation)

```
Shift-start PPE and fatigue screening in Northern Ontario mining remains manual,
inconsistent, and undocumented. Existing computer vision systems detect personal
protective equipment (PPE) globally but fail to account for zone-specific
requirements under Ontario Regulation 854 — producing false alarms when workers
enter surface areas where hard hats are not required.

We present Northern Shift Guard, a three-layer vision-language decision framework
for explainable and auditable shift-start safety screening. Given a worker photo
and selected mine zone, the system: (1) extracts structured PPE and fatigue
evidence via GPT-4o vision, (2) checks detections against zone-specific compliance
rules, and (3) reasons over evidence using NVIDIA Nemotron to produce prioritized
supervisor actions grounded in regulatory context. Every decision is stored in an
audit log with full evidence chain.

We evaluate on [N] images across [M] mine zones and show that zone-aware
compliance reduces false alarm rates by [X]% compared to global-rule baselines,
while maintaining [Y]% PPE detection accuracy. A zone-flip case study
demonstrates that identical visual evidence yields different compliance outcomes
under surface vs active stope requirements. We discuss limitations including
fatigue screening as a visual aid (not medical diagnosis), privacy considerations,
and deployment requirements for production mine sites.
```

### One-sentence pitch (for abstract / intro)

> Northern Shift Guard is an explainable, zone-aware, auditable shift-start screening system for Northern Ontario mines — not a black box.

---

## Paper structure

### Full outline

```
1. Introduction
   1.1 Motivation: shift-start safety gap in Northern Ontario mining
   1.2 Limitations of global PPE detection
   1.3 Contributions (C1–C5)
   1.4 Paper organization

2. Related Work
   2.1 PPE detection in industrial and mining settings
   2.2 Vision-language models for safety violation detection
   2.3 Explainable and auditable AI in regulated domains
   2.4 Positioning vs MonitorVLM and related systems

3. Problem Formulation
   3.1 Mine zones and PPE requirements (Ontario Reg 854)
   3.2 Decision outputs: compliance, action, audit record
   3.3 Human-in-the-loop constraints and scope

4. Method
   4.1 System overview (reference architecture diagram)
   4.2 Vision evidence extraction (GPT-4o structured JSON)
   4.3 Zone compliance engine (config-driven rules)
   4.4 Nemotron reasoning over evidence + regulation context
   4.5 Audit log schema and traceability
   4.6 Frontend and deployment (brief)

5. Experimental Setup
   5.1 Datasets (public PPE + curated mining-relevant set)
   5.2 Baselines
   5.3 Metrics
   5.4 Evaluation protocol

6. Results
   6.1 PPE detection performance
   6.2 Zone-flip accuracy and false alarm reduction
   6.3 Reasoning quality (supervisor rubric scores)
   6.4 Ablation studies
   6.5 Latency and cost analysis

7. Discussion
   7.1 Implications for shift-start workflows
   7.2 Fatigue screening scope and limitations
   7.3 Privacy, consent, and deployment ethics
   7.4 Production requirements (offline fallback, checkpoint lighting)

8. Limitations and Future Work
   8.1 Dataset size and domain shift
   8.2 Real-time capture and batch crew scanning
   8.3 Expanded PPE types and analytics

9. Conclusion

Appendix (optional)
   A. Zone configuration schema
   B. Prompt templates
   C. Sample audit records
   D. Supervisor evaluation rubric
```

### Must-have figures

| Figure | Source | Description |
|--------|--------|-------------|
| **Fig 1** | `docs/system_architecture.svg` | End-to-end pipeline |
| **Fig 2** | `submission_media/05_demo_scan_results.jpg` | UI: detection + compliance + action |
| **Fig 3** | New — zone-flip experiment | Same image × 2 zones → different verdicts |
| **Fig 4** | New — evaluation results | Bar chart: false alarms global vs zone-aware |
| **Fig 5** | `submission_media/08_audit_trail.jpg` | Audit trail example |
| **Table 1** | `backend/config/zones.json` | Zone PPE requirements |
| **Table 2** | New | Baseline comparison metrics |

---

## Evaluation plan

### Phase 1 — Dataset construction (Week 1–2)

**Target size:** 150–300 images minimum for arXiv; 300+ for industry conference.

| Source | Size | Purpose |
|--------|------|---------|
| **Public PPE datasets** | 100–200 | SH17, Construction-PPE, jhboyo/ppe-dataset |
| **Curated mining/industrial photos** | 30–50 | Domain-relevant scenarios with manual labels |
| **Existing demo set** | 10 | `sample_images/` — seed cases |
| **Synthetic zone assignments** | All | Label each image with applicable zone(s) |

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
  "source": "sh17 | construction_ppe | curated | demo"
}
```

**Public datasets to use:**

| Dataset | Link | Classes |
|---------|------|---------|
| SH17 | [GitHub](https://github.com/ahmadmughees/SH17dataset) | Helmet, Safety-vest, Person, Head |
| Construction-PPE | [Ultralytics](https://docs.ultralytics.com/datasets/detect/construction-ppe/) | helmet/no_helmet, vest/no_vest |
| jhboyo/ppe-dataset | [Hugging Face](https://huggingface.co/datasets/jhboyo/ppe-dataset) | helmet, head, vest |

### Phase 2 — Baselines (Week 2–3)

| Baseline | Description | Expected weakness |
|----------|-------------|-------------------|
| **B1: Global rules** | Hard hat + hi-vis always required | False alarms on surface zone |
| **B2: Vision-only** | GPT-4o pass/fail, no zone context | No zone-specific guidance |
| **B3: YOLO + global rules** | YOLOv8 PPE detector + global compliance | No reasoning; false alarms |
| **B4: Full pipeline** | Northern Shift Guard (vision + zone + Nemotron) | Target system |

### Phase 3 — Metrics (Week 3–4)

| Metric | Definition | Target |
|--------|------------|--------|
| **PPE detection accuracy** | Correct hard_hat / hi_vis labels vs ground truth | Report per-class precision/recall |
| **Zone-flip accuracy** | Correct compliance when zone changes for same image | Key headline metric |
| **False alarm reduction** | (Global false alarms − Zone-aware false alarms) / Global | Quantify C4 |
| **Reasoning quality score** | Supervisor rubric (1–5) on action correctness, grounding, clarity | Mean ± std over N cases |
| **End-to-end latency** | Upload → full response time | Report p50, p95 |
| **Cost per scan** | API cost (GPT-4o + Nemotron) per analysis | USD per scan |

### Phase 4 — Zone-flip experiment (headline result)

**Protocol:**

1. Select 20–30 images where hard hat is **absent** but worker is otherwise compliant
2. Run each image through pipeline with zone = **Surface / Yard**
3. Run same image with zone = **Active Stope**
4. Record compliance verdict and supervisor action for each

**Expected result:**

| Zone | Hard hat required? | Verdict | Action |
|------|-------------------|---------|--------|
| Surface / Yard | No | ✅ Compliant | No immediate action |
| Active Stope | Yes | ❌ Non-compliant | Stop-work before underground entry |

**Report:** False alarm rate of global baseline vs zone-aware system on this subset.

### Phase 5 — Ablation studies

| Ablation | Compare | Question |
|----------|---------|----------|
| Zone context in Nemotron prompt | w/ vs w/o `zone_context_for_prompt()` | Does zone context improve action quality? |
| Safety reference text | w/ vs w/o `data/safety_refs/` | Does regulatory context improve grounding? |
| Reasoning model | Nemotron vs GPT-4o-mini fallback | Quality vs cost tradeoff |
| Vision model | GPT-4o vs YOLO (if trained) | Accuracy vs latency tradeoff |

### Phase 6 — Reasoning quality evaluation

**Supervisor rubric (1–5 scale):**

| Criterion | 1 (Poor) | 5 (Excellent) |
|-----------|----------|---------------|
| **Action correctness** | Wrong priority or action | Correct stop-work / monitor / pass |
| **Regulatory grounding** | No reference to zone rules | Cites zone requirements appropriately |
| **Explainability clarity** | Opaque or generic | Clear chain: seen → requires → do |
| **Practical usability** | Supervisor couldn't act on this | Actionable steps provided |

**Protocol:**

- Select 25–30 scan results across pass/fail/fatigue/zone-flip cases
- Rate independently by 3 reviewers (team + 1 domain contact if possible)
- Report inter-rater agreement and mean scores per criterion

---

## Target venues (PhD application strategy)

Prioritize venues that (a) don't require US in-person attendance, (b) reach ML/NLP/XAI faculty, and (c) produce a citable artifact for your application.

### Scope fit scale (1–5)

How well Northern Shift Guard matches each venue **at current project scope** (prototype + planned eval, no user study yet).

| Score | Label | Meaning |
|-------|-------|---------|
| **4.5 – 5.0** | **High likelihood** | Strong fit; submit with confidence once eval is done |
| **3.5 – 4.4** | **Likely** | Good fit; competitive but realistic with solid M1–M4 results |
| **2.5 – 3.4** | **Moderate** | Partial fit; needs extra experiments or reframing |
| **1.5 – 2.4** | **Stretch** | Significant gaps; only try with major additions |
| **< 1.5** | **Unlikely** | Poor fit at current scale; deprioritize |

*Score = scope fit + acceptance realism. arXiv scores 5.0 because there is no peer-review gate.*

---

### All venues — scope fit & acceptance likelihood

| Venue | Type | Scope fit | Acceptance likelihood | Travel? | PhD ROI |
|-------|------|-----------|----------------------|---------|---------|
| **arXiv** (`cs.AI` + `cs.IR`) | Preprint | **5.0 / 5** | **High** — no peer review; you have endorsement | No | ⭐⭐⭐ |
| **AAAI AISI workshop** | Workshop | **4.0 / 5** | **Likely** — applied XAI + social impact | Varies | ⭐⭐⭐ |
| **ACL/EMNLP NLP-app workshop** | Workshop | **4.0 / 5** | **Likely** — RAG + structured LLM output | Often hybrid | ⭐⭐⭐ |
| **NeurIPS Safe ML / AI4SG workshop** | Workshop | **3.5 / 5** | **Likely** — needs strong zone-flip eval + ablations | Often hybrid | ⭐⭐⭐ |
| **ICML ML4Eng workshop** | Workshop | **3.5 / 5** | **Likely** — decision-support systems angle | Often hybrid | ⭐⭐⭐ |
| **NeurIPS main track** | Conference | **2.0 / 5** | **Stretch** — SOTA-scale benchmark expected | Yes | ⭐⭐⭐ |
| **EMNLP Findings** | Conference | **2.5 / 5** | **Stretch** — needs deeper RAG/reasoning ablations | Varies | ⭐⭐⭐ |
| **FAccT** | Conference | **3.0 / 5** | **Moderate** — audit trail fits; needs accountability framing | Varies | ⭐⭐⭐ |
| **AIES** | Conference | **3.0 / 5** | **Moderate** — regulated-domain ethics angle | Varies | ⭐⭐⭐ |
| **CHI** | Conference | **2.0 / 5** | **Stretch** — needs supervisor trust/UX user study (n≥15) | Yes | ⭐⭐ |
| **CVPR/ICCV main track** | Conference | **1.5 / 5** | **Unlikely** — large vision benchmark + SOTA required | Yes | ⭐⭐ |
| **SME MINEXCHANGE** | Industry | **4.0 / 5** | **N/A — deprioritized** (visa + mandatory US talk) | Yes (USA) | ⭐ |
| **CIM / OneMine** | Industry | **3.5 / 5** | **N/A — deprioritized** (wrong PhD audience) | Varies | ⭐ |

### Recommended submission order

```
1. arXiv (cs.AI + cs.IR)      ← first, after M4 results
2. AAAI AISI or ACL workshop  ← best workshop odds (4.0)
3. NeurIPS / ICML workshop    ← if CFP timing aligns (3.5)
4. FAccT / AIES               ← only with accountability extras (3.0)
5. Skip CHI, CVPR main, SME   ← unless scope expands significantly
```

---

### Tier 1 — Primary (do these)

| Venue | Scope fit | Acceptance | Why |
|-------|-----------|------------|-----|
| **arXiv** | **5.0** | **High** | Citable artifact; matches your **`cs.AI` + `cs.IR` endorsements** |
| **ACL/EMNLP workshops** | **4.0** | **Likely** | RAG over safety refs + structured LLM = `cs.IR` + `cs.AI` story |
| **AAAI AISI workshop** | **4.0** | **Likely** | Explainable regulated-AI; applied systems welcome |
| **NeurIPS/ICML workshops** | **3.5** | **Likely** | Safe ML / ML4Eng — competitive but realistic with eval |

### Tier 2 — Strong if eval is solid

| Venue | Scope fit | Acceptance | What you'd need to add |
|-------|-----------|------------|------------------------|
| **FAccT** | **3.0** | **Moderate** | Accountability framing; optional user trust study |
| **AIES** | **3.0** | **Moderate** | Ethics of automated decisions; human-in-the-loop analysis |
| **EMNLP Findings** | **2.5** | **Stretch** | RAG ablation (with/without safety refs), reasoning metrics |
| **CHI** | **2.0** | **Stretch** | Supervisor UX/trust study — **not high chance at current scope** |

### Tier 3 — Deprioritized

| Venue | Scope fit | Why skip |
|-------|-----------|----------|
| **NeurIPS / ICML main track** | **2.0** | Benchmark bar too high for current eval scale |
| **CVPR/ICCV main track** | **1.5** | Vision-SOTA expectations; wrong contribution framing |
| **SME MINEXCHANGE** | **4.0*** | *Good industry fit but visa blocker + wrong PhD audience |
| **CIM / OneMine** | **3.5*** | *Mining audience, not CS PhD admissions |

---

### arXiv — your endorsements

You have **`cs.AI`** and **`cs.IR`** endorsements. Submit under both.

| Category | Endorsed? | Emphasize in paper |
|----------|-----------|-------------------|
| **cs.AI** | ✅ Yes | Multi-stage reasoning, VLM→LLM pipeline, structured output, zone-aware logic |
| **cs.IR** | ✅ Yes | RAG over `data/safety_refs/`, retrieval-augmented regulatory grounding |
| cs.CL | ❌ No | Mention LLM/NLP in text; don't request — no endorsement |
| cs.CV | ❌ No | Vision is one stage; not primary framing |
| cs.CY | ❌ No | Discuss XAI/audit in body instead |

**Submit as:** `cs.AI` + `cs.IR`

**Keyword alignment:**
- `cs.AI` → "vision-language reasoning", "structured decision pipeline", "explainable AI"
- `cs.IR` → "retrieval-augmented generation", "regulatory context retrieval", "grounded LLM actions"

Requesting categories without endorsement can delay arXiv posting. **`cs.AI` + `cs.IR` both fit naturally** — RAG is explicitly an IR contribution.

### Paper title reframing (PhD vs industry)

| ❌ Industry framing | ✅ PhD framing |
|---------------------|----------------|
| "Mining Shift-Start Safety Screening" | "Context-Aware Vision-Language Reasoning for Auditable Decision Support" |
| "PPE Detection for Northern Ontario Mines" | "From Detection to Decision: Structured Evidence + LLM Reasoning + Audit Trails" |
| "Ontario Reg 854 Compliance Tool" | "Grounded LLM Actions with Retrieval-Augmented Regulatory Context" |

Suggested title for arXiv:
> **From Visual Evidence to Grounded Action: A Zone-Aware Vision-Language Framework with Retrieval-Augmented Reasoning and Auditable Decision Chains**

Mining application goes in abstract §2–3, not the title.

### How to use this in PhD applications

| Application piece | What to highlight |
|-------------------|-------------------|
| **Research statement / SOP** | 3-layer XAI architecture; zone-flip as context-sensitivity result; RAG over safety refs |
| **CV — Publications** | arXiv preprint (once live); workshop paper if accepted |
| **CV — Projects** | GitHub + demo URL + eval metrics |
| **Emails to professors** | 2-sentence pitch + arXiv link; mention overlap with their XAI/NLP/RAG work |
| **Portfolio website** | Architecture diagram, zone-flip figure, audit trail screenshot |

**Skills demonstrated:** structured LLM output, VLM integration, RAG, rule-based + neural hybrid, evaluation design, full-stack ML system.

---

## Target venues (archived — industry track)

### Tier 1 — Primary targets

| Venue | Type | Deadline | Fit | Notes |
|-------|------|----------|-----|-------|
| **arXiv** | Preprint | Rolling | ✅ Excellent | cs.CV, cs.AI, or cs.CY; no peer review |
| **CIM Convention** | Industry | ~Feb–Mar annually | ✅ Excellent | Canadian mining; strong Reg 854 relevance |
| **SME MINEXCHANGE 2027** | Industry | Abstract **Aug 1, 2026** · notify **Oct 31** · manuscript **Nov 15** (optional) | ✅ Excellent | Presentations mandatory; conference Feb 28 – Mar 3, 2027, Denver |
| **OneMine** | Technical publication | Rolling | ✅ Excellent | Peer-reviewed mining technical papers |

### Tier 2 — Secondary targets

| Venue | Type | Fit | Notes |
|-------|------|-----|-------|
| **NeurIPS Safe ML Workshop** | ML workshop | ✅ Good | If evaluation is strong |
| **AAAI AI for Social Impact** | Workshop | ✅ Good | Explainable AI angle |
| **IEEE AI for Industry** | Applied | ✅ Good | Industrial deployment focus |
| **ICML ML4Eng Workshop** | Workshop | ✅ Good | Engineering decision support |

### Tier 3 — Stretch targets

| Venue | Fit | Requirements |
|-------|-----|--------------|
| **CHI** | ⚠️ Possible | Needs supervisor UX + trust study |
| **ICRA/IROS** | ⚠️ Possible | Needs real-time/robotics angle |
| **CVPR/ICCV main track** | ❌ Unlikely | Needs large benchmark + SOTA comparison |

### arXiv categories

- **cs.CV** — Computer Vision and Pattern Recognition
- **cs.AI** — Artificial Intelligence
- **cs.CY** — Computers and Society (regulatory/audit angle)
- **cs.LG** — Machine Learning (if emphasizing ablations)

### Mining industry conference submission tips

- Lead with **real-world problem** and **Ontario Reg 854** grounding
- Include **deployment architecture** and **audit trail** as differentiators
- Emphasize **human-in-the-loop** — not replacing supervisors
- Provide **demo URL** or **Docker instructions** for reproducibility
- Include **limitations section** prominently — industry reviewers respect honesty
- Consider co-authorship with a **mining safety professional** if available

---

## Timeline & milestones

### PhD-focused calendar

| When | Milestone | Deliverable |
|------|-----------|-------------|
| **Now** | M1 Dataset | 50–150 labeled images |
| **+2–3 weeks** | M2–M3 Eval + figures | Zone-flip results, baseline comparison |
| **+4 weeks** | M4–M5 arXiv | Preprint live — **before PhD application deadlines** |
| **+6–8 weeks** | M6 Workshop | Submit to NeurIPS/ACL/AAAI workshop (check CFP dates) |

Target: **arXiv live by Fall 2026** so it's on your CV for PhD applications (most deadlines Dec 2026 – Jan 2027).

### Archived — SME calendar (deprioritized)

| Date | Event | What to deliver |
|------|-------|-----------------|
| **Now → Jul 2026** | M1 Dataset | Build eval set (`eval/dataset/`) |
| **Jul 2026** | M2–M5 (parallel if time) | Baselines, figures, arXiv draft — strengthens abstract but **not required** for Aug 1 |
| **August 1, 2026** | **Abstract deadline** | 100-word abstract → submit at [smeannualconference.org](https://smeannualconference.org) |
| **Aug – Oct 2026** | Continue M2–M5 | Full eval + optional manuscript prep |
| **October 31, 2026** | **Acceptance notification** | If accepted → prepare presentation |
| **November 15, 2026** | **Final manuscripts due** | Optional — submit `paper/main.tex` PDF if desired |
| **Nov 2026 – Feb 2027** | Presentation prep | Slides, demo, zone-flip figure (mandatory if accepted) |
| **February 28 – March 3, 2027** | **Conference** | Present in Denver |

**Important:** Manuscripts are **not mandatory**. Presentations of accepted abstracts **are mandatory**.

### 4-week fast path (arXiv)

| Week | Milestone | Deliverable |
|------|-----------|-------------|
| **1** | Dataset construction | 150+ labeled images, eval schema |
| **2** | Baselines + metrics | Eval notebook with B1–B4 results |
| **3** | Zone-flip + ablations | Headline figures and tables |
| **4** | Paper draft + arXiv submit | LaTeX PDF on arXiv |

### 8-week path (arXiv + industry conference)

| Week | Milestone | Deliverable |
|------|-----------|-------------|
| **1–2** | Dataset + baselines | Full eval pipeline |
| **3–4** | Zone-flip + ablations + reasoning eval | All results tables/figures |
| **5–6** | Paper draft v1 | Complete LaTeX manuscript |
| **7** | Internal review + revisions | v2 with feedback incorporated |
| **8** | arXiv submit + conference submit | Both submissions |

### Milestone checklist

- [ ] Evaluation dataset (150+ images) with labels
- [ ] Eval notebook with reproducible metrics
- [ ] Baseline comparison results (B1–B4)
- [ ] Zone-flip experiment figure
- [ ] Ablation study results
- [ ] Reasoning quality scores (3 reviewers)
- [ ] Latency/cost analysis
- [ ] LaTeX paper draft
- [ ] All figures at publication quality (300 DPI)
- [ ] arXiv submission
- [ ] Industry conference submission

---

## Repository assets for research

### Code to reference in paper

| Component | File | Section |
|-----------|------|---------|
| Zone compliance engine | `backend/zone_service.py` | §4.3 |
| Zone definitions | `backend/config/zones.json` | §4.3, Table 1 |
| Vision service | `backend/vision_service.py` | §4.2 |
| Nemotron reasoning | `backend/nemotron_service.py` | §4.4 |
| Prompts | `backend/prompts.py` | Appendix B |
| Audit log | `backend/db.py` | §4.5 |
| API schema | `backend/schemas.py` | §4.5 |
| Model config | `backend/config/model_config.json` | §5.1 |

### Data assets

| Asset | Location | Use |
|-------|----------|-----|
| Safety references | `data/safety_refs/` | Nemotron context; cite in §4.4 |
| Demo images | `sample_images/` | Qualitative examples |
| Zone config | `backend/config/zones.json` | Table 1 |

### Documentation to repurpose

| Doc | Location | Repurpose as |
|-----|----------|--------------|
| Master plan | `docs/PLAN.md` | §3 Problem, §4 Method |
| Devpost story | `docs/devpost_story.md` | §1 Introduction |
| Project report | `docs/Northern_Shift_Guard_Project_Report.pdf` | Background sections |
| Architecture diagram | `docs/system_architecture.svg` | Figure 1 |
| Pitch notes | `docs/pitch_mobile.txt` | Demo script, Q&A prep |

### Figures from submission media

| Image | Use |
|-------|-----|
| `submission_media/07_app_dashboard.jpg` | System overview figure |
| `submission_media/05_demo_scan_results.jpg` | Results UI figure |
| `submission_media/08_audit_trail.jpg` | Audit trail figure |
| `submission_media/Demo_Analysis1.png` | Zone-flip case study |

---

## Suggested folder layout

Create this structure when starting the paper:

```
Cursor_Hackathon/
├── docs/
│   └── RESEARCH.md                  ← this file
├── paper/
│   ├── README.md                    ← build instructions for LaTeX
│   ├── main.tex                     ← paper source
│   ├── references.bib               ← BibTeX references
│   ├── figures/
│   │   ├── architecture.pdf         ← from system_architecture.svg
│   │   ├── zone_flip.pdf            ← new: headline figure
│   │   ├── results_bar.pdf          ← new: evaluation results
│   │   └── audit_trail.pdf          ← from submission_media
│   └── sections/
│       ├── abstract.tex
│       ├── introduction.tex
│       ├── related_work.tex
│       ├── method.tex
│       ├── experiments.tex
│       ├── results.tex
│       ├── discussion.tex
│       └── conclusion.tex
├── eval/
│   ├── README.md                    ← evaluation protocol
│   ├── dataset/
│   │   ├── labels.json              ← ground truth labels
│   │   └── images/                  ← eval image set
│   ├── baselines/
│   │   ├── global_rules.py
│   │   ├── vision_only.py
│   │   ├── yolo_global.py
│   │   └── full_pipeline.py
│   ├── metrics/
│   │   ├── ppe_detection.py
│   │   ├── zone_flip.py
│   │   └── reasoning_quality.py
│   └── results/
│       ├── tables/                  ← CSV/LaTeX tables
│       └── figures/                 ← generated plots
└── notebooks/
    └── northern_shift_guard.ipynb   ← extend with eval cells
```

---

## Writing checklist

### Before writing

- [ ] Read MonitorVLM paper and 2–3 related works
- [ ] Finalize evaluation results (don't write results section without data)
- [ ] Prepare all figures at 300 DPI
- [ ] Set up LaTeX template (IEEE or conference-specific)

### Abstract (150–250 words)

- [ ] Problem statement (1–2 sentences)
- [ ] Gap in existing approaches (1 sentence)
- [ ] Our approach / contributions (2–3 sentences)
- [ ] Key results with numbers (2 sentences)
- [ ] Limitations acknowledged (1 sentence)

### Introduction

- [ ] Hook: shift-start safety gap in Northern Ontario
- [ ] Problem: manual, undocumented, zone-blind checks
- [ ] Gap: global PPE detectors don't account for zone context
- [ ] Contributions: C1–C5 listed explicitly
- [ ] Paper organization paragraph

### Method

- [ ] Architecture diagram (Figure 1)
- [ ] Each layer described with enough detail to reproduce
- [ ] Zone config schema documented
- [ ] Prompt templates referenced (Appendix)
- [ ] Audit log schema documented

### Experiments

- [ ] Dataset described with size, sources, label schema
- [ ] Baselines clearly defined
- [ ] Metrics defined mathematically
- [ ] Evaluation protocol reproducible

### Results

- [ ] Zone-flip figure (headline result)
- [ ] Baseline comparison table
- [ ] Ablation results
- [ ] Reasoning quality scores
- [ ] Latency/cost table

### Discussion

- [ ] Implications for mining operations
- [ ] Comparison to related work
- [ ] Limitations stated honestly
- [ ] Future work scoped realistically

---

## Limitations to state explicitly

Reviewers and industry audiences respect honest scoping. Include all of these:

| Limitation | How to frame it |
|------------|-----------------|
| **Fatigue is screening only** | Visual aid, not medical diagnosis; supervisor remains decision-maker |
| **Small evaluation set** | Hackathon-origin prototype; production needs larger mine-site dataset |
| **Cloud API dependency** | MVP uses GPT-4o + Nemotron APIs; production needs offline fallback |
| **No real mine-site deployment** | Prototype validated on public + curated images; field trial is future work |
| **Limited PPE types** | Hard hat + hi-vis only; gloves, respirators, boots are roadmap |
| **Lighting conditions** | Vision quality degrades in low-light underground; checkpoint lighting needed |
| **Privacy / consent** | Production requires retention policy, role-based access, union agreements |
| **Not replacing supervisors** | Decision support tool; all safety decisions remain human |
| **Domain shift** | Public PPE datasets are construction/manufacturing; mining transfer is approximate |

---

## Next actions

> **Current focus: Milestone 1 — Dataset construction.**  
> See [`eval/dataset/README.md`](../eval/dataset/README.md) for the full checklist.

### M1 — Dataset (you are here)

1. Create `eval/dataset/images/` subfolders
2. Label all `sample_images/` files
3. Add real image for `zone_flip_no_hardhat`
4. Download public PPE dataset (SH17 or jhboyo)
5. Sample, label, and append to `labels.json`
6. Hit ≥ 50 images (150 for arXiv)
7. Sign off M1 checklist → then proceed to M2

### Later milestones (do not start yet)

- **M2:** Run baselines B1–B4 on full dataset
- **M3:** Generate zone-flip figure
- **M4:** Reframe paper for XAI/NLP audience; fill `paper/sections/results.tex`
- **M5:** Submit **arXiv** preprint (primary goal)
- **M6:** Submit to ML/NLP workshop (NeurIPS / ACL / AAAI — check CFPs)
- ~~**SME MINEXCHANGE:**~~ Deprioritized — visa + wrong audience

---

## References (starter BibTeX)

Add to `paper/references.bib`:

```bibtex
@article{monitorvlm2025,
  title={MonitorVLM: A Vision Language Framework for Safety Violation Detection in Mining Operations},
  journal={arXiv preprint arXiv:2510.03666},
  year={2025}
}

@article{mdse2026,
  title={From 3D Perception to Safety Reasoning: A Graph-Based Framework for Real-Time Underground Mine Monitoring},
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
```

---

## Contact & collaboration

For research collaboration, domain expert review, or mining site partnership inquiries:

- **Kaysarul Anas Apurba** — architecture, backend, evaluation
- **Kazeem Oguntade** — domain framing, industry outreach

**GitHub:** [repository URL]  
**Demo:** [deployed URL if available]  
**Hackathon gallery:** [Cursor Hackathon Sudbury 2026 winners](https://cheickis.github.io/cursor-hackathon-sudbury-2026/winners/#gallery)
