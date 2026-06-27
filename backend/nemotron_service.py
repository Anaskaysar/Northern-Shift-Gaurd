import json
from pathlib import Path

import httpx
from openai import OpenAI

from prompts import NEMOTRON_SYSTEM_PROMPT
from schemas import NemotronAction, VisionAnalysis
from settings import get_settings


def load_safety_context() -> str:
    refs_dir = Path(__file__).resolve().parent.parent / "data" / "safety_refs"
    if not refs_dir.exists():
        return "Follow standard Northern Ontario mine-site PPE requirements: hard hat and hi-vis vest required in active zones."
    chunks = []
    for path in sorted(refs_dir.glob("*.txt")):
        chunks.append(path.read_text(encoding="utf-8").strip())
    return "\n\n".join(chunks) if chunks else "Use standard mine-site PPE and fatigue screening policies."


def reason_mock(vision: VisionAnalysis) -> NemotronAction:
    if vision.ppe.hard_hat == "fail":
        return NemotronAction(
            priority="stop_work",
            supervisor_action="Stop work immediately — verify hard hat compliance before operator enters the active zone.",
            rationale="Missing hard hat is a critical PPE violation near machinery.",
            recommended_steps=[
                "Halt operator movement into the work zone",
                "Issue compliant hard hat and re-check before entry",
                "Log incident in shift safety record",
            ],
        )
    if vision.ppe.hi_vis == "fail":
        return NemotronAction(
            priority="intervene",
            supervisor_action="Hold floor entry until high-visibility vest is confirmed.",
            rationale="Hi-vis vest missing reduces visibility in industrial traffic areas.",
            recommended_steps=[
                "Provide compliant vest",
                "Re-scan before allowing floor access",
            ],
        )
    if vision.fatigue.risk in {"medium", "high"}:
        return NemotronAction(
            priority="monitor",
            supervisor_action="Assign closer supervision and consider a brief rest break — fatigue screening flag only.",
            rationale="Visible fatigue cues detected; not equivalent to a PPE stop-work event.",
            recommended_steps=[
                "Brief supervisor check-in with operator",
                "Monitor for next 30 minutes",
                "Do not use as medical diagnosis",
            ],
        )
    return NemotronAction(
        priority="none",
        supervisor_action="No immediate action required — PPE compliance appears satisfactory.",
        rationale="Hard hat and hi-vis checks passed with low fatigue risk.",
        recommended_steps=["Continue routine shift-start monitoring"],
    )


def reason_nvidia(vision: VisionAnalysis) -> NemotronAction:
    settings = get_settings()
    safety_context = load_safety_context()
    payload = {
        "vision_evidence": vision.model_dump(),
        "safety_reference_context": safety_context,
    }

    with httpx.Client(timeout=60.0) as client:
        response = client.post(
            "https://integrate.api.nvidia.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.nvidia_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "nvidia/nemotron-mini-4b-instruct",
                "messages": [
                    {"role": "system", "content": NEMOTRON_SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": json.dumps(payload),
                    },
                ],
                "temperature": 0.2,
                "max_tokens": 600,
            },
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        data = json.loads(content)
        return NemotronAction(**data)


def reason_openai_fallback(vision: VisionAnalysis) -> NemotronAction:
    settings = get_settings()
    if not settings.openai_api_key:
        return reason_mock(vision)

    client = OpenAI(api_key=settings.openai_api_key)
    safety_context = load_safety_context()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": NEMOTRON_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "vision_evidence": vision.model_dump(),
                        "safety_reference_context": safety_context,
                    }
                ),
            },
        ],
        response_format={"type": "json_object"},
        max_tokens=600,
    )
    data = json.loads(response.choices[0].message.content or "{}")
    return NemotronAction(**data)


def reason_over_evidence(vision: VisionAnalysis) -> tuple[NemotronAction, str]:
    settings = get_settings()
    provider = settings.nemotron_provider.lower()

    if provider == "nvidia" and settings.nvidia_api_key:
        try:
            return reason_nvidia(vision), "nvidia"
        except Exception:
            pass

    if settings.openai_api_key:
        return reason_openai_fallback(vision), "openai"

    return reason_mock(vision), "mock"
