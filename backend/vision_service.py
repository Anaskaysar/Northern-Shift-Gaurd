import json
import replicate
from schemas import VisionAnalysis, PPEResult, FatigueResult, EvidenceItem
from prompts import VISION_SYSTEM_PROMPT
from settings import get_settings


def _parse(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def _mock_vision() -> tuple[VisionAnalysis, str]:
    return VisionAnalysis(
        ppe=PPEResult(hard_hat="unclear", hi_vis="unclear"),
        fatigue=FatigueResult(risk="unclear", indicators=[]),
        evidence=[EvidenceItem(region="system", observation="Vision model unavailable — check REPLICATE_API_TOKEN", severity="warning")],
        explanation="Mock result — no vision API key configured.",
    ), "mock"


def analyze_vision(image_data_url: str) -> tuple[VisionAnalysis, str]:
    settings = get_settings()

    if not settings.replicate_api_token:
        return _mock_vision()

    import os
    os.environ["REPLICATE_API_TOKEN"] = settings.replicate_api_token

    try:
        output = replicate.run(
            "yorickvp/llava-13b:b5f6212d032508382d61ff00469ddda3e32fd8a0755a17f6664032f16c9a0a07",
            input={
                "image": image_data_url,
                "prompt": VISION_SYSTEM_PROMPT,
                "max_tokens": 600,
                "temperature": 0.1,
            },
        )
        raw = "".join(output) if hasattr(output, "__iter__") else str(output)
        data = _parse(raw)

        return VisionAnalysis(
            ppe=PPEResult(**data["ppe"]),
            fatigue=FatigueResult(**data.get("fatigue", {"risk": "unclear", "indicators": []})),
            evidence=[EvidenceItem(**e) for e in data.get("evidence", [])],
            explanation=data.get("explanation", ""),
        ), "replicate"

    except Exception as e:
        print(f"[Vision] Replicate error: {e}")
        v, _ = _mock_vision()
        v.evidence = [EvidenceItem(region="system", observation=f"Vision model error: {e}", severity="warning")]
        return v, "mock"
