export type PPEStatus = "pass" | "fail" | "unclear";
export type FatigueRisk = "low" | "medium" | "high" | "unclear";
export type Priority = "none" | "monitor" | "intervene" | "stop_work";
export type ComplianceStatus = "compliant" | "non_compliant" | "not_required";

export interface EvidenceItem {
  region: string;
  observation: string;
  severity: "info" | "warning" | "critical";
}

export interface ZoneRequirement {
  ppe_item: string;
  label: string;
  required: boolean;
  detected: PPEStatus;
  compliant: ComplianceStatus;
}

export interface ZoneCompliance {
  zone_id: string;
  zone_name: string;
  regulation: string;
  requirements: ZoneRequirement[];
  overall: "compliant" | "non_compliant";
}

export interface AnalyzeResponse {
  scan_id: number;
  vision: {
    ppe: { hard_hat: PPEStatus; hi_vis: PPEStatus };
    fatigue: { risk: FatigueRisk; indicators: string[] };
    evidence: EvidenceItem[];
    explanation: string;
  };
  zone_compliance: ZoneCompliance | null;
  nemotron: {
    priority: Priority;
    supervisor_action: string;
    rationale: string;
    recommended_steps: string[];
  };
  provider: { vision: string; nemotron: string };
  image_filename: string;
  created_at: string;
}

export interface ScanSummary {
  id: number;
  image_filename: string;
  hard_hat: PPEStatus;
  hi_vis: PPEStatus;
  fatigue_risk: FatigueRisk;
  priority: Priority;
  supervisor_action: string;
  zone_id: string | null;
  zone_name: string | null;
  created_at: string;
}

export interface ZoneDefinition {
  name: string;
  description: string;
  required_ppe: string[];
  fatigue_check: boolean;
  regulation: string;
}
