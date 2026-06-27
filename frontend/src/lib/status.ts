import type { AnalyzeResponse, PPEStatus, Priority } from "../types";

export type Decision = "pass" | "conditional" | "fail" | "pending";

export const DECISION_META: Record<
  Decision,
  { label: string; tone: "pass" | "conditional" | "fail" | "pending" }
> = {
  pass: { label: "Pass", tone: "pass" },
  conditional: { label: "Conditional", tone: "conditional" },
  fail: { label: "Fail", tone: "fail" },
  pending: { label: "Pending review", tone: "pending" },
};

export function computeOverallDecision(result: AnalyzeResponse): Decision {
  const { vision, nemotron } = result;

  if (nemotron.priority === "stop_work") return "fail";
  if (vision.ppe.hard_hat === "fail" || vision.ppe.hi_vis === "fail") return "fail";
  if (nemotron.priority === "intervene") return "fail";
  if (vision.fatigue.risk === "high") return "conditional";
  if (nemotron.priority === "monitor") return "conditional";
  if (vision.ppe.hard_hat === "unclear" || vision.ppe.hi_vis === "unclear") return "conditional";
  if (vision.fatigue.risk === "medium") return "conditional";
  return "pass";
}

export function decisionFromScan(priority: Priority, hardHat: PPEStatus, hiVis: PPEStatus): Decision {
  if (priority === "stop_work" || hardHat === "fail" || hiVis === "fail" || priority === "intervene") {
    return "fail";
  }
  if (priority === "monitor" || hardHat === "unclear" || hiVis === "unclear") {
    return "conditional";
  }
  return "pass";
}

export function ppeStatusLabel(status: PPEStatus): string {
  if (status === "pass") return "Present";
  if (status === "fail") return "Missing";
  return "Unclear";
}

export function ppeStatusTone(status: PPEStatus): "pass" | "conditional" | "fail" {
  if (status === "pass") return "pass";
  if (status === "fail") return "fail";
  return "conditional";
}

export function fatigueTone(risk: string): "pass" | "conditional" | "fail" | "pending" {
  if (risk === "low") return "pass";
  if (risk === "medium") return "conditional";
  if (risk === "high") return "fail";
  return "pending";
}

export function priorityLabel(priority: Priority): string {
  return priority.replace("_", " ");
}
