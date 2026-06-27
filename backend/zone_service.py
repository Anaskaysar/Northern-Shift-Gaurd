import json
from pathlib import Path
from schemas import ZoneCompliance, ZoneRequirement, VisionAnalysis

_ZONES_PATH = Path(__file__).resolve().parent / "config" / "zones.json"

PPE_LABELS = {
    "hard_hat": "Hard Hat",
    "hi_vis": "Hi-Vis Vest",
}


def load_zones() -> dict:
    return json.loads(_ZONES_PATH.read_text())


def check_zone_compliance(zone_id: str, vision: VisionAnalysis) -> ZoneCompliance:
    zones = load_zones()

    if zone_id not in zones:
        zone_id = "surface"

    zone = zones[zone_id]
    required_ppe: list[str] = zone["required_ppe"]

    detected = {
        "hard_hat": vision.ppe.hard_hat,
        "hi_vis": vision.ppe.hi_vis,
    }

    requirements = []
    overall_compliant = True

    for ppe_item, label in PPE_LABELS.items():
        required = ppe_item in required_ppe
        status = detected.get(ppe_item, "unclear")

        if not required:
            compliance = "not_required"
        elif status == "pass":
            compliance = "compliant"
        else:
            # fail or unclear when required → non-compliant
            compliance = "non_compliant"
            overall_compliant = False

        requirements.append(ZoneRequirement(
            ppe_item=ppe_item,
            label=label,
            required=required,
            detected=status,
            compliant=compliance,
        ))

    return ZoneCompliance(
        zone_id=zone_id,
        zone_name=zone["name"],
        regulation=zone["regulation"],
        requirements=requirements,
        overall="compliant" if overall_compliant else "non_compliant",
    )


def zone_context_for_prompt(zone_id: str) -> str:
    zones = load_zones()
    if zone_id not in zones:
        return ""
    z = zones[zone_id]
    required = " and ".join(PPE_LABELS[p] for p in z["required_ppe"])
    return (
        f"Zone: {z['name']} — {z['description']}. "
        f"Required PPE for this zone: {required}. "
        f"Regulation: {z['regulation']}."
    )
