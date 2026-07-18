"""Baseline B4: Full Northern Shift Guard zone-aware compliance (standalone)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

ZONES_PATH = Path(__file__).resolve().parent.parent.parent / "backend" / "config" / "zones.json"
PPE_LABELS = {"hard_hat": "Hard Hat", "hi_vis": "Hi-Vis Vest"}


@dataclass
class ComplianceResult:
    overall: str
    false_alarm: bool


def _load_zones() -> dict:
    return json.loads(ZONES_PATH.read_text())


def evaluate_zone_aware(
    hard_hat: str,
    hi_vis: str,
    zone_id: str,
    ground_truth_compliant: bool,
) -> ComplianceResult:
    """Zone compliance check mirroring backend/zone_service.py."""
    zones = _load_zones()
    if zone_id not in zones:
        zone_id = "surface"

    zone = zones[zone_id]
    required_ppe = set(zone["required_ppe"])
    detected = {"hard_hat": hard_hat, "hi_vis": hi_vis}
    overall_compliant = True

    for ppe_item in PPE_LABELS:
        required = ppe_item in required_ppe
        status = detected.get(ppe_item, "unclear")

        if required and status != "pass":
            overall_compliant = False

    overall = "compliant" if overall_compliant else "non_compliant"
    false_alarm = overall == "non_compliant" and ground_truth_compliant
    return ComplianceResult(overall=overall, false_alarm=false_alarm)
