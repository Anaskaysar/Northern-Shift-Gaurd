# Northern Shift Guard

**Team:** NorthMind  
**Track:** Mining & Industrial Innovation  
**Event:** Cursor Hackathon Sudbury 2026 — Build the North

## One-sentence pitch

An explainable AI safety system for Northern Ontario mining sites that detects PPE non-compliance and fatigue risk, reasons over evidence with Nemotron, and stores every flagged decision in TiDB — no black boxes.

## Architecture

```
Image upload
  → Vision model (Replicate) → structured JSON { hard_hat, hi_vis, fatigue_risk, evidence[] }
  → Nemotron → prioritized supervisor action (plain language)
  → TiDB / SQLite → full audit trail
  → UI: pass/fail badge + evidence cards + supervisor action
```

## Stack

| Layer | Tool |
|-------|------|
| IDE | Cursor |
| Vision inference | Replicate |
| Reasoning | Nemotron (NVIDIA) |
| Audit storage | TiDB Cloud (SQLite fallback for local dev) |
| Safety context | Apify-scraped refs in `data/safety_refs/` |
| Backend | FastAPI (Python) |
| Frontend | React + Vite (industrial UI via Lovable) |
| Model work | Jupyter notebook |

## Project structure

```
├── backend/           FastAPI API (vision, Nemotron, audit log)
├── frontend/          React dashboard
├── notebooks/         Model eval + prompt tuning
├── data/safety_refs/  Mining/OSHA safety context for Nemotron
├── sample_images/     Demo photos for testing
├── docs/              Plan, resume, event reference (see docs/README.md)
```

**Planning:** see [`docs/PLAN.md`](docs/PLAN.md) for the full execution plan, remaining tasks, and submission checklist.

## Setup

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env   # fill in your keys
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 and upload a photo from `sample_images/`.

## API

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check |
| `POST /api/analyze` | Image → PPE + fatigue JSON + Nemotron action |
| `GET /api/scans` | Scan history from audit log |

## Demo

1. Upload `sample_images/pass_compliant.jpg` → green pass
2. Upload `sample_images/fail_missing_hardhat.jpg` → fail + stop-work action
3. Upload `sample_images/fatigue_tired_operator.jpg` → fatigue flag + monitor action
4. Open **Audit trail** tab to show stored scan history

## Disclaimer

Fatigue screening is a visual aid only — not a medical diagnosis.
