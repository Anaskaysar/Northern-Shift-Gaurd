# Northern Shift Guard

**Team:** NorthMind  
**Track:** Mining & Industrial Innovation  
**Event:** Cursor Hackathon Sudbury 2026 — Build the North

## One-sentence pitch

An explainable AI safety system for Northern Ontario mining sites that detects PPE non-compliance and fatigue risk, checks compliance against zone-specific requirements, reasons over evidence with Nemotron, and stores every flagged decision in a local audit log — no black boxes.

## Architecture

```
Supervisor selects mine zone (e.g. Active Stope)
  → Upload worker photo
  → Vision model (OpenAI GPT-4o) → structured JSON { hard_hat, hi_vis, fatigue_risk, evidence[] }
  → Zone rules engine → per-item required / detected / compliant
  → Nemotron → zone-tailored supervisor action (plain language)
  → SQLite audit log → full scan history
  → UI: detection cards + zone compliance panel + Nemotron action
```

## Stack

| Layer | Tool |
|-------|------|
| IDE | Cursor |
| Vision inference | OpenAI (GPT-4o) |
| Reasoning | Nemotron (NVIDIA) |
| Audit storage | SQLite (local / deployed) |
| Safety context | Apify-scraped refs in `data/safety_refs/` |
| Backend | FastAPI (Python) |
| Frontend | React + Vite (industrial UI via Lovable) |
| Model work | Jupyter notebook |

## Project structure

```
├── backend/           FastAPI API (vision, Nemotron, zone rules, audit log)
├── frontend/          React dashboard
├── notebooks/         Model eval + prompt tuning
├── data/safety_refs/  Mining/OSHA safety context for Nemotron
├── sample_images/     Demo photos for testing
├── docs/              Plan, resume, event reference (see docs/README.md)
```

**Planning:** see [`docs/PLAN.md`](docs/PLAN.md) for the full execution plan, remaining tasks, and submission checklist.

## Setup

```bash
# Quick start (both servers)
./run.sh

# Or manually:
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

Open http://localhost:5173, select a mine zone, and upload a photo from `sample_images/`.

## API

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check |
| `GET /api/zones` | Mine zone definitions and PPE requirements |
| `POST /api/analyze` | Image + zone → vision JSON + zone compliance + Nemotron action |
| `GET /api/scans` | Scan history from audit log |

## Demo (~3 min)

1. Select **Active Stope / Production Zone**
2. Upload `sample_images/fail_missing_hardhat.jpg` → hard hat fail, zone non-compliant, Nemotron stop-work action
3. Switch zone to **Surface / Yard**, re-upload same image → hard hat not required; outcome may differ
4. Upload `sample_images/pass_compliant.jpg` in Open Pit → green compliant
5. Upload `sample_images/fatigue_tired_operator.jpg` → fatigue flag + monitor action
6. Open **Audit trail** tab → stored scans with zone, evidence JSON, and Nemotron action

**Key judge moment:** same photo, different zone → different compliance verdict.

## Deploy

Production runs as a single Docker container (FastAPI serves API + built React UI).

```bash
# Build and run locally
docker build -t northern-shift-guard .
docker run -p 8000:8000 --env-file .env northern-shift-guard
```

Open http://localhost:8000

**Render (recommended):** connect this repo on [Render](https://render.com), choose **Web Service → Docker**, set env vars from `.env.example`, deploy. See `render.yaml` for blueprint.

Required env vars: `OPENAI_API_KEY`, `VISION_PROVIDER=openai`, `NVIDIA_API_KEY` (or `NEMOTRON_PROVIDER=mock` for demo without Nemotron).

## Disclaimer

Fatigue screening is a visual aid only — not a medical diagnosis.
