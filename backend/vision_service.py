import json
import replicate
from openai import OpenAI
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
        evidence=[EvidenceItem(region="system", observation="Vision model unavailable — check API keys", severity="warning")],
        explanation="Mock result — no vision API key configured.",
    ), "mock"


def _analyze_openai(image_data_url: str, settings) -> tuple[VisionAnalysis, str]:
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": VISION_SYSTEM_PROMPT},
                    {"type": "image_url", "image_url": {"url": image_data_url}},
                ],
            }
        ],
        response_format={"type": "json_object"},
        max_tokens=600,
        temperature=0.1,
    )
    data = json.loads(response.choices[0].message.content or "{}")
    return VisionAnalysis(
        ppe=PPEResult(**data["ppe"]),
        fatigue=FatigueResult(**data.get("fatigue", {"risk": "unclear", "indicators": []})),
        evidence=[EvidenceItem(**e) for e in data.get("evidence", [])],
        explanation=data.get("explanation", ""),
    ), "openai"


def _analyze_replicate(image_data_url: str, settings) -> tuple[VisionAnalysis, str]:
    import os
    os.environ["REPLICATE_API_TOKEN"] = settings.replicate_api_token
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


def analyze_vision(image_data_url: str) -> tuple[VisionAnalysis, str]:
    settings = get_settings()
    provider = settings.vision_provider.lower()

    # OpenAI (GPT-4o vision)
    if provider == "openai" and settings.openai_api_key:
        try:
            return _analyze_openai(image_data_url, settings)
        except Exception as e:
            print(f"[Vision] OpenAI error: {e}")

    # Replicate (LLaVA-13B)
    if provider == "replicate" and settings.replicate_api_token:
        try:
            return _analyze_replicate(image_data_url, settings)
        except Exception as e:
            print(f"[Vision] Replicate error: {e}")

    # Auto-detect: try OpenAI first, then Replicate
    if provider == "mock":
        if settings.openai_api_key:
            try:
                return _analyze_openai(image_data_url, settings)
            except Exception as e:
                print(f"[Vision] OpenAI error: {e}")
        if settings.replicate_api_token:
            try:
                return _analyze_replicate(image_data_url, settings)
            except Exception as e:
                print(f"[Vision] Replicate error: {e}")

    return _mock_vision()
