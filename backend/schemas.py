from __future__ import annotations
from typing import List, Literal, Optional
from pydantic import BaseModel

PPEStatus = Literal["pass", "fail", "unclear"]
FatigueRiskLevel = Literal["low", "medium", "high", "unclear"]
Priority = Literal["none", "monitor", "intervene", "stop_work"]
Severity = Literal["info", "warning", "critical"]
ComplianceStatus = Literal["compliant", "non_compliant", "not_required"]


class PPEResult(BaseModel):
    hard_hat: PPEStatus
    hi_vis: PPEStatus


class FatigueResult(BaseModel):
    risk: FatigueRiskLevel
    indicators: List[str] = []


class EvidenceItem(BaseModel):
    region: str
    observation: str
    severity: Severity


class VisionAnalysis(BaseModel):
    ppe: PPEResult
    fatigue: FatigueResult
    evidence: List[EvidenceItem] = []
    explanation: str = ""


class ZoneRequirement(BaseModel):
    ppe_item: str               # e.g. "hard_hat"
    label: str                  # e.g. "Hard Hat"
    required: bool
    detected: PPEStatus
    compliant: ComplianceStatus


class ZoneCompliance(BaseModel):
    zone_id: str
    zone_name: str
    regulation: str
    requirements: List[ZoneRequirement]
    overall: Literal["compliant", "non_compliant"]


class NemotronAction(BaseModel):
    priority: Priority
    supervisor_action: str
    rationale: str
    recommended_steps: List[str] = []


class ProviderInfo(BaseModel):
    vision: str
    nemotron: str


class AnalyzeResponse(BaseModel):
    scan_id: int
    vision: VisionAnalysis
    zone_compliance: Optional[ZoneCompliance] = None
    nemotron: NemotronAction
    provider: ProviderInfo
    image_filename: str
    created_at: str


class ScanSummary(BaseModel):
    id: int
    image_filename: str
    hard_hat: PPEStatus
    hi_vis: PPEStatus
    fatigue_risk: FatigueRiskLevel
    priority: Priority
    supervisor_action: str
    zone_id: Optional[str] = None
    zone_name: Optional[str] = None
    created_at: str
