import base64
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import AnalyzeResponse, ProviderInfo
from vision_service import analyze_vision
from nemotron_service import reason_over_evidence
from db import save_scan, get_recent_scans
from settings import get_settings

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


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    image_bytes = await file.read()
    data_url = f"data:{file.content_type};base64,{base64.b64encode(image_bytes).decode()}"

    # Vision
    vision, vision_provider = analyze_vision(data_url)

    # Nemotron reasoning
    nemotron, nemotron_provider = reason_over_evidence(vision)

    # Build response (no scan_id yet)
    result = AnalyzeResponse(
        scan_id=0,
        vision=vision,
        nemotron=nemotron,
        provider=ProviderInfo(vision=vision_provider, nemotron=nemotron_provider),
        image_filename=file.filename or "upload",
        created_at="",
    )

    # Persist and get real scan_id
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
