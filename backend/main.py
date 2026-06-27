import base64
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Optional

from schemas import AnalyzeResponse, ProviderInfo
from vision_service import analyze_vision
from nemotron_service import reason_over_evidence
from zone_service import check_zone_compliance, zone_context_for_prompt, load_zones
from db import save_scan, get_recent_scans
from settings import get_settings, ROOT_DIR

settings = get_settings()

app = FastAPI(title="Northern Shift Guard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "project": "Northern Shift Guard", "team": "NorthMind"}


@app.get("/api/zones")
def get_zones():
    return load_zones()


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze(
    file: UploadFile = File(...),
    zone: Optional[str] = Form(default="open_pit"),
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    image_bytes = await file.read()
    data_url = f"data:{file.content_type};base64,{base64.b64encode(image_bytes).decode()}"

    # Vision
    vision, vision_provider = analyze_vision(data_url)

    # Zone compliance check
    zone_compliance = check_zone_compliance(zone or "open_pit", vision)

    # Nemotron reasoning — enriched with zone context
    zone_ctx = zone_context_for_prompt(zone or "open_pit")
    nemotron, nemotron_provider = reason_over_evidence(vision, zone_ctx)

    result = AnalyzeResponse(
        scan_id=0,
        vision=vision,
        zone_compliance=zone_compliance,
        nemotron=nemotron,
        provider=ProviderInfo(vision=vision_provider, nemotron=nemotron_provider),
        image_filename=file.filename or "upload",
        created_at="",
    )

    try:
        scan_id = save_scan(result)
        result.scan_id = scan_id
    except Exception as e:
        print(f"[DB] save_scan failed: {e}")
        result.scan_id = -1

    return result


@app.get("/api/scans")
def scans(limit: int = 20):
    try:
        return get_recent_scans(limit=limit)
    except Exception as e:
        print(f"[DB] get_recent_scans failed: {e}")
        return []


# Serve built React UI in production (Docker / Render)
_static_dir = ROOT_DIR / "frontend" / "dist"
if _static_dir.is_dir():
    app.mount("/", StaticFiles(directory=_static_dir, html=True), name="frontend")
